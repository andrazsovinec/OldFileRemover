import argparse
import re
import os
import time
from datetime import datetime

def parse_duration(duration):
    duration_pattern = re.compile(r'(?P<value>\d+)(?P<unit>[YMDhms])')
    match = duration_pattern.fullmatch(duration.strip())
    if not match:
        raise ValueError(f"Invalid duration format: {duration}")
    
    value = int(match.group('value'))
    unit = match.group('unit')
    
    duration_dict = {
        'Y': value * 365 * 24 * 3600,  # Years to seconds
        'M': value * 30 * 24 * 3600,   # Months to seconds (approximation)
        'D': value * 24 * 3600,        # Days to seconds
        'h': value * 3600,             # Hours to seconds
        'm': value * 60,               # Minutes to seconds
        's': value                    # Seconds
    }
    
    if unit not in duration_dict:
        raise ValueError(f"Invalid duration unit: {unit}")
    
    return duration_dict[unit]

def get_file_creation_time(file_path):
    
    creation_time = os.path.getctime(file_path)
    
    return round(creation_time)

def delete_old_files_and_empty_folders(folder_path, time_threshold, initial_call=True):
    
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path):
            delete_old_files_and_empty_folders(item_path, time_threshold, initial_call=False)
        elif os.path.isfile(item_path):
            creation_time = get_file_creation_time(item_path)
            if creation_time < time_threshold:
                print(f"Deleting file: {item_path}")
                os.remove(item_path)

    if not initial_call and not os.listdir(folder_path):
        print(f"Deleting empty folder: {folder_path}")
        os.rmdir(folder_path)

parser = argparse.ArgumentParser(description="Accept folder and duration.")
parser.add_argument("folder", type=str, help="The folder path.")
parser.add_argument("duration", type=str, help="The duration (e.g., '1Y', '3D', '300s').")

args = parser.parse_args()
folder = args.folder
duration = parse_duration(args.duration)
max_age = round(time.time() - duration)

print(f"Folder: {folder}")
print(f"Duration in seconds: {duration}")
print(f"Max age in seconds: {max_age}")

delete_old_files_and_empty_folders(folder, max_age, True)
