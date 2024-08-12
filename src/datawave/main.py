import get_data
import json
import argparse
import os
import get_data
import run_analysis_file
import pandas as pd

def read_json(file_path):
    with open(file_path, 'r') as f:
        field_name_dict = json.load(f)
    return dict(field_name_dict)



parser = argparse.ArgumentParser(description='Data retrieval and analysis.')

# Separate flags for each type of input
parser.add_argument('--data-file', '-d', required=True, help='File name to the data file (e.g., .mat, .nwb, .txt).')
parser.add_argument('--analysis-folder', '-p', required=False, help='File name to the Python file for custom processing.')
parser.add_argument('--json-file', '-j', required=False, help='File name to the JSON configuration file.')

args = parser.parse_args()

# Input files
data_file = args.data_file
python_file = args.analysis_folder
json_file = args.json_file


supported_ext = [".mat", ".nwb", ".csv", ".txt", ".adicht", ".rhd"]


# Extract the file extension
data_file_ext = os.path.splitext(data_file)[1].lower()

# Ensure data file has a supported extension
if data_file_ext not in supported_ext:
    raise ValueError(f"Unsupported data file extension: {data_file_ext}")

try:
    field_name_dict = read_json(json_file)
except Exception as e:
    print(f"No json file found: {e}")
    field_name_dict = {}

get_final_df = get_data.run(data_file_ext, data_file, field_name_dict)

if get_final_df is None:
    get_final_df = pd.DataFrame()

# Save the DataFrame to a CSV file
csv_file_path = "derived_file.csv"
get_final_df.to_csv(csv_file_path, index=False)


## run python analysis code
run_analysis_file.run(python_file, get_final_df)
