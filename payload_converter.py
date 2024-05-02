import json
import os
import pandas as pd
from datetime import datetime

def process_payload_data(payload_test):
    # Attempt to load the configuration file
    try:
        with open("outputPayloadConfig.json", 'r', encoding="utf8") as f:
            output_payload_config = json.load(f)
    except Exception as e:
        error = f"Error: {e}"
        return error

    output_dir = "output"
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Process each item in the payload
    for item in payload_test:
        try:
            item_config = output_payload_config[item["name"]]
            item_hexa = item["hexaValue"][22:-4]
            temp_dict = {'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            
            last_character_count = 0
            
            for field in item_config:
                field_name = field["name"]
                field_length = field["characterCount"]
                field_value_hex = item_hexa[last_character_count:last_character_count + field_length]
                field_value_decimal = int(field_value_hex, 16) / field["divisionFactor"]
                temp_dict[field_name] = field_value_decimal
                last_character_count += field_length

            output_file_path = os.path.join(output_dir, f"{item['name']}.csv")
            
            # Check if the file exists
            if os.path.exists(output_file_path):
                # If the file exists, load it, append the new data, and save it
                existing_data = pd.read_csv(output_file_path)
                new_row = pd.DataFrame([temp_dict])
                updated_data = pd.concat([existing_data, new_row], ignore_index=True)
                updated_data.to_csv(output_file_path, index=False)
            else:
                # If the file does not exist, create a new CSV with headers
                new_data = pd.DataFrame([temp_dict])
                new_data.to_csv(output_file_path, index=False)
        
        except Exception as e:
            error = f"Error: {e}"
            return error
        
    msg = f"Success! All files are now updated!"
    return msg