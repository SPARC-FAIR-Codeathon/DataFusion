import scipy.io
import numpy as np


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
            raise ValueError("Required fields are not present in the .mat file")


def read_mat(data_file, field_name_dictionary):
    mat = scipy.io.loadmat(data_file)
    return process_mat_file(mat, field_name_dictionary)

# def plot_time_series(series, time_data):
#     plt.plot(time_data, series)

# plot_time_series(series[0, :1000], time_data[0,:1000])