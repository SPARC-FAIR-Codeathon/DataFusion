import scipy.io
import numpy as np
import subprocess
import shutil

def process_mat_file(mat, field_name_dictionary):
    if "Time Series" in field_name_dictionary.keys():
        series_key = field_name_dictionary["Time Series"]

        if "Time stamps" in field_name_dictionary.keys():
            time_data_key = field_name_dictionary["Time stamps"]

            series = mat[series_key]
            time_data = mat[time_data_key]

            return series, time_data


        elif "Sampling Frequency" in field_name_dictionary.keys() and "Start Time" in field_name_dictionary.keys():
            sf_key = field_name_dictionary["Sampling Frequency"]
            sf = mat[sf_key]
            start_time_key = mat["Start Time"]

            start_time = mat[start_time_key]
            length = mat[series_key].shape[0]
            time_data = np.arange(start_time, start_time + length / sf, 1 / sf)

            series = mat[series_key]

            return series, time_data

        elif "Sampling Frequency" in field_name_dictionary.keys():
            sf_key = field_name_dictionary["Sampling Frequency"]
            sf = mat[sf_key]

            length = mat[series_key].shape[0]
            time_data = np.arange(length) / sf
            series = mat[series_key]

            return series, time_data

        else:
            return None, None


def add_other_labels(mat_file, field_name_dictionary, df):
    if field_name_dictionary:  ## only proceed if it is not empty
        exclude = {"Time stamps", "Time Series", "Sampling Frequency"}
        filtered_dict = {k: v for k, v in field_name_dictionary.items() if k not in exclude}
        if filtered_dict:  ## only proceed if it is not empty
            for key in filtered_dict:
                if len(df) == len(mat_file[key]):
                    df[key] = mat_file[key]

    return df


def read_mat(data_file, field_name_dictionary):
    mat = scipy.io.loadmat(data_file)
    return process_mat_file(mat, field_name_dictionary)


def convert_mat_to_h5(data_file):
    command = f"python3 mat2h5.py {data_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    # move file
    shutil.move("converted.h5", "extra_derived_files")


