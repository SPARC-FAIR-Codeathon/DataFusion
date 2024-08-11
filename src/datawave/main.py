import get_data
import json
import argparse
import os
import get_data

def read_json(file_path):
    with open(file_path, 'r') as f:
        field_name_dict = json.load(f)
    return dict(field_name_dict)



parser = argparse.ArgumentParser(description='Data retrieval and analysis.')

# Separate flags for each type of input
parser.add_argument('--data-file', '-d', required=True, help='File name to the data file (e.g., .mat, .nwb, .txt).')
parser.add_argument('--python-file', '-p', required=True, help='File name to the Python file for custom processing.')
parser.add_argument('--json-file', '-j', required=True, help='File name to the JSON configuration file.')

args = parser.parse_args()

# Input files
data_file = args.data_file
python_file = args.python_file
json_file = args.json_file


supported_ext = [".mat", ".nwb", ".csv", ".txt", ".adicht", ".rhd"]


# Extract the file extension
data_file_ext = os.path.splitext(data_file)[1].lower()

# Ensure data file has a supported extension
if data_file_ext not in supported_ext:
    raise ValueError(f"Unsupported data file extension: {data_file_ext}")

field_name_dict = read_json(json_file)
get_final_df = get_data.run(data_file_ext, data_file, field_name_dict)

# # Create an output directory
# output_dir = 'output'
# os.makedirs(output_dir, exist_ok=True)
#
# # Set the output file prefix
# output_prefix = os.path.join(output_dir, os.path.splitext(os.path.basename(data_file))[0])

# Save the DataFrame to a CSV file
csv_file_path = f"derived_file.csv"
get_final_df.to_csv(csv_file_path, index=False)

print("files saved successfully")