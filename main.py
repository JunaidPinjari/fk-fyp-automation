import time
import json
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from payload_converter import process_payload_data

def get_config_data():
    try:
        with open("config.json", 'r', encoding="utf8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Error while reading config file: {e}")
        exit(1)

def create_chrome_instance(headless):
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        if headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        return driver
    except Exception as e:
        print(f"Failed to create a Chrome driver instance: {e}")
        exit(1)

def go_to_url(driver):
    try:
        login_url = "https://sharedwmc.wanesy.com/#/login"
        driver.get(login_url)
        if driver.current_url != login_url:
            return False
        return True
    except Exception as e:
        print(f"Failed to navigate to {login_url}: {e}")
        return False

def login(driver, username, password):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys(username)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        login_button = driver.find_element(By.ID, "loginButton")
        login_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "home")))
    except Exception as e:
        print(f"Login failed: {e}")

def get_data(driver, port, payloads):
    
    output_payload_json = []

    for payload_item in payloads:
        # data down input section starts

        down_page_url = "https://sharedwmc.wanesy.com/#/end-devices/506F980000003872/data-down"
        driver.get(down_page_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "endDeviceDataDown")))

        add_btn = driver.find_element(By.XPATH, '//i[@class="icon-add"]')
        add_btn.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fPort")))
        port_input = driver.find_element(By.ID, "fPort")
        port_input.send_keys(port)
        payload_input = driver.find_element(By.ID, "payload")
        payload_input.send_keys(payload_item["payload"])
        validate_btn = driver.find_element(By.ID, "dataDownForm-validate")
        validate_btn.click()
        time.sleep(5)
        # data down input section ends


        # data up output section starts
        up_page_url = "https://sharedwmc.wanesy.com/#/end-devices/506F980000003872/data-up"
        driver.get(up_page_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "endDeviceDataUp")))

        first_row = driver.find_element(By.XPATH, '//*[@id="endDeviceDataUpGrid"]/div[2]/table/tbody/tr[1]')
        first_row.click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="detailsModal___BV_modal_body_"]/div/div[3]/div')))
        output_payload = driver.find_element(By.XPATH, '//*[@id="detailsModal___BV_modal_body_"]/div/div[3]/div').text
        print(output_payload)
        output_payload_json.append(
            {
                "name": payload_item["name"],
                "hexaValue": output_payload
            }
        )
        time.sleep(2)
        # data up output section ends

    return output_payload_json

def output_to_csv(output_payload_json):
    response = process_payload_data(output_payload_json)
    print(response)

def terminate_chrome_instance(driver):
    try:
        driver.quit()
    except Exception as e:
        print(f"Failed to close the Chrome driver: {e}")

def main(config):
    driver = None
    try:
        driver = create_chrome_instance(config["headless"])
        if go_to_url(driver):
            login(driver, config["username"], config["password"])
            output_payload_json = get_data(driver, config["port"], config["payloads"])
            output_to_csv(output_payload_json)
        else:
            raise Exception("Error while fetching website URL.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if driver:
            terminate_chrome_instance(driver)

if __name__ == "__main__":
    config = get_config_data()
    interval_seconds = config.get("interval_minutes", 30) * 60  # Default to 30 minutes if not specified
    hours_count = config.get("hours_count", 24)  # Default to 24 hours if not specified
    end_time = datetime.now() + timedelta(hours=hours_count)  # Calculate when to stop the loop

    if interval_seconds == 0:
        main(config)  # If interval is 0, run once immediately
    else:
        while datetime.now() < end_time:
            main(config)
            time.sleep(interval_seconds)