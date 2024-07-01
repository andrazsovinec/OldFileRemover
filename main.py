import argparse
from dateutil.relativedelta import relativedelta
import re

# Function to parse the duration string
def parse_duration(duration):
    duration_pattern = re.compile(
        r'(?:(?P<years>\d+?)\s*years?)?'
        r'(?:(?P<months>\d+?)\s*months?)?'
        r'(?:(?P<weeks>\d+?)\s*weeks?)?'
        r'(?:(?P<days>\d+?)\s*days?)?'
        r'(?:(?P<hours>\d+?)\s*hours?)?'
        r'(?:(?P<minutes>\d+?)\s*minutes?)?'
        r'(?:(?P<seconds>\d+?)\s*seconds?)?'
    )
    match = duration_pattern.fullmatch(duration.strip())
    if not match:
        raise ValueError(f"Invalid duration format: {duration}")
    
    duration_dict = {key: int(value) for key, value in match.groupdict().items() if value}
    return relativedelta(**duration_dict)

# Setup argument parser
parser = argparse.ArgumentParser(description="Accept folder and duration.")
parser.add_argument("folder", type=str, help="The folder path.")
parser.add_argument("duration", type=str, help="The duration (e.g., '1 year 2 months 3 days 4 hours 5 minutes 6 seconds').")

# Parse arguments
args = parser.parse_args()
folder = args.folder
duration = parse_duration(args.duration)

# Print out the variables
print(f"Folder: {folder}")
print(f"Duration: {duration}")
