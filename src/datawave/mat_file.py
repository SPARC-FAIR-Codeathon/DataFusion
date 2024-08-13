import scipy.io
import numpy as np
import os
import shutil

def process_mat_file(mat, field_name_dictionary):
    """
    :param mat- loaded mat file
    :param field_name_dictionary- field name dictionary
    :return series and time data based on field name dictionary and create pseudo time stamps wherever applicable
    """
    if "Time Series" in field_name_dictionary.keys():
        series_key = field_name_dictionary["Time Series"]

        if "Time stamps" in field_name_dictionary.keys():
            time_data_key = field_name_dictionary["Time stamps"]

            series = mat[series_key]
            time_data = mat[time_data_key]

            return series, time_data

        ## if sampling frequency and starting time is given use that
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


def add_other_labels(data_file, field_name_dictionary, df):
    """
    Adds extra labels such as behavioural for machine learning and other things
    :param data_file- mat data file name
    :param field_name_dictionary- field name dictionaries
    :param df- data frame containing time series and time stamps
    """

    if field_name_dictionary:  ## only proceed if it is not empty
        mat = scipy.io.loadmat(data_file) 
        exclude = {"Time stamps", "Time Series", "Sampling Frequency"}
        filtered_dict = {k: v for k, v in mat.items() if k not in exclude}
        if filtered_dict:  ## only proceed if it is not empty
            for key in filtered_dict:            
                if len(df) == len(mat[key]):
                    df[key] = mat[key]

    return df


def read_mat(data_file, field_name_dictionary):
    """
    return the loaded mat file
    :param data_file- the name of the mat file
    :param field_name_dictionary- field name dictionary from JSON containing the field names to be stored in csv
    """
    mat = scipy.io.loadmat(data_file)
    return process_mat_file(mat, field_name_dictionary)


def convert_mat_to_h5(data_file):
    """
    convert the data_file to h5 and stores it in correct location as extra_derived_files
    """
    command = f"python3 mat2h5.py {data_file}"
    os.system(command)
    
    # move file
    shutil.move("converted.h5", "extra_derived_files")


