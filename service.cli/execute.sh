#!/bin/sh
# set sh strict mode
set -o errexit
set -o nounset
IFS=$(printf '\n\t')

cd /home/scu/datawave

echo "starting service as"
echo   User    : "$(id "$(whoami)")"
echo   Workdir : "$(pwd)"
echo "..."
echo
# ----------------------------------------------------------------
# This script shall be modified according to the needs in order to run the service
# The inputs defined in ${INPUT_FOLDER}/inputs.json are available as env variables by their key in capital letters
# For example: input_1 -> $INPUT_1

# Copy input data file
echo "Getting data file from input_1..."
num_datafile=$(find "${INPUT_FOLDER}" \( -type f -name "*.mat" -o -name "*.txt" -o -name "*.rhd" -o -name "*.adicht" -o -name "*.nwb" \) | wc -l)

if [ "$num_datafile" = 1 ]; then
    filen="$(find "${INPUT_FOLDER}" \( -type f -name "*.mat" -o -name "*.txt" -o -name "*.rhd" -o -name "*.adicht" -o -name "*.nwb" \))"
    cp "$filen" .
    dat_filen="$(basename "${filen}")"
else
    echo "Please provide only one data file"
    exit 1
fi


echo "Finding the analysis_py folder..."

# Find the folder named analysis_py
analysis_py_folder=$(find "${INPUT_FOLDER}" -type d -name "analysis_py")

if [ -d "$analysis_py_folder" ]; then
    echo "Folder found: $analysis_py_folder"
    cp -r "$analysis_py_folder" .
else
    echo "Folder named analysis_py not found. Creating it..."
    mkdir -p "analysis_py"
    echo "Folder created: analysis_py"
fi


echo "Getting Json file from input_3..."
num_jsonfile=$(find "${INPUT_FOLDER}" \( -type f -name "*.json" \) | wc -l)

if [ "$num_jsonfile" -eq 1 ]; then
    filen="$(find "${INPUT_FOLDER}" \( -type f -name "*.json" \))"
    cp "$filen" .
    json_filen="$(basename "${filen}")"
elif [ "$num_jsonfile" -eq 0 ]; then
    echo "No JSON file found. Creating an empty JSON file."
    echo "{}" > empty.json
    json_filen="empty.json"
else
    echo "Please provide only one json file"
    exit 1
fi


# put the code to execute the service here
# For example:
#env
#ls -al "${INPUT_FOLDER}"

# Launch data retrieval and analysis
echo "Starting data retrieval"
mkdir "extra_derived_files" # to store extra files such as nwb file

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
# shellcheck source=/dev/null
. venv/bin/activate

# Install necessary pip packages
echo "Installing necessary pip packages..."
pip install --upgrade pip

echo "Setting virtual environment permissions..."
chmod -R u+rwx venv

# Check if the file extension is rhd and prompt to install neuroconv
if [ "${dat_filen##*.}" = "rhd" ]; then
    echo "File extension is .rhd. neuroconv is required for processing."
    echo "Installing requirements...it will take some time"
    pip --quiet install -r requirements_rhd.txt


else
    echo "Installing requirements...it will take some time"
    pip --quiet install -r requirements.txt
fi
echo "Successfully installed"

python3 main.py  \
  -d "$dat_filen" \
  -p "analysis_py" \
  -j "$json_filen" 

echo "Analysis and retrieval completed successfully, adding it to the output..."
# Add derived_files to output

zip -rj -FS "${OUTPUT_FOLDER}/derived_files.zip" "derived_file.csv" "extra_derived_files" "derived_analysis"

