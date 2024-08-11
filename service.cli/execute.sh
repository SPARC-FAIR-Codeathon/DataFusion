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


echo "Getting Python file from input_2..."
num_pyfile=$(find "${INPUT_FOLDER}" \( -type f -name "*.py" \) | wc -l)

if [ "$num_pyfile" = 1 ]; then
    filen="$(find "${INPUT_FOLDER}" \( -type f -name "*.py" \))"
    cp "$filen" .
    analysis_filen="$(basename "${filen}")"
else
    echo "Please provide only one Python file"
    exit 1
fi


echo "Getting Json file from input_3..."
num_pyfile=$(find "${INPUT_FOLDER}" \( -type f -name "*.json" \) | wc -l)

if [ "$num_pyfile" = 1 ]; then
    filen="$(find "${INPUT_FOLDER}" \( -type f -name "*.json" \))"
    cp "$filen" .
    json_filen="$(basename "${filen}")"
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
git clone https://github.com/neurogarg/DataWave.git
cd DataWave
python3 main.py \
    -i "$dat_filen" \
    -i "$analysis_filen" \
    -i "$json_filen"
echo "Analysis and retrieval completed successfully, adding it to the output..."
# Add derived_files to output

zip -r "${OUTPUT_FOLDER}"/derived_files.zip "derived_file.csv" "sample_plot.png" "analysis_plot.png"



