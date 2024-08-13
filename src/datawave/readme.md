## Backend Python scripts to convert the input files into a common format and to run Python script.

`main.py`: The main Python script that is being executed by the (shell commands)[https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/service.cli/execute.sh]. It takes input data, JSON file and python analysis folder as input and returns a CSV file or NWB file (wherever implemened) and outputs of the pyhon analysis script. All the outputs are ultimately zipped by shell commands. 
`get_data.py`: The secondary Python script that returns a pandas dataframe and saved NWB, H5. The returned df are saved as CSV by `main.py`
`utils.py`: converts time series and time stamps to CSV files.
`rhd_file.py`, `mat_file.py`, `adicht_file.py`: main processing scripts for .rhd, .mat, .adicht file formats.
`requirements.txt`, `requirements_rhd.txt`: List of general and .rhd specific dependencies.
`run_analysis_file.py`: is a wrapper script that runs the user-defined analysis.py file.
`mat2h5.py`: utils to convert mat to h5 format
`importrhdutilities.py` utils to read .rhd file format


