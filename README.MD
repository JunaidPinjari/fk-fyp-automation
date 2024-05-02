# Automated Browser Interaction with Selenium

## Project Overview
This project automates the login and data retrieval process from a specified web application using Selenium. The script logs into `https://sharedwmc.wanesy.com`, navigates through various pages, performs data entry, and retrieves payload information, which is then processed and outputted in a csv format.

## Features
- **Automated Login:** Automatically logs into the web portal.
- **Data Entry and Retrieval:** Enters necessary data and retrieves output from dynamic web pages.
- **Data Processing:** Processes the retrieved data and outputs it in a csv format.

## Dependencies
The script relies on several Python packages:
- `selenium`: For automating web browser interaction.
- `webdriver-manager`: Simplifies the management of binary drivers for browsers.
- `pandas`: For writing processed data to csv.
- `json`: For parsing JSON files that contain configuration data.

Ensure that Python 3.10+ is installed on your machine.

## Installation
1. Clone the repository: `git clone https://github.com/JunaidPinjari/fk-fyp-automation.git`
2. Navigate to the project directory
3. Install dependencies: `pip install -r requirements.txt`

## Configuration
1. Before running the script, head to config.json and make necessary changes such as username, password etc. 
    - Set headless to false, to view browser while running and for debugging.
    - interval_minutes defines the interval in minutes the script should automatically run in.
    - hours_count defines the total number of hours the script should run for and following which should automatically stop.
    - Set interval_minutes to 0, to run only once immediately without loop.

2. Leave outputPayloadConfig.json as is, unless you know what you're doing.

## Running the script
1. Once you're through with the setup, run: `python main.py`