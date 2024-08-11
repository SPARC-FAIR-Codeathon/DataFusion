import os
import utils
import mat_file


def run(data_file_ext, data_file, field_name_dictionary):
    supported_ext = [".mat", ".nwb", ".csv", ".txt", ".adicht", ".rhd"]

    if data_file_ext == supported_ext[0]:
        series, time_data = mat_file.read_mat(data_file, field_name_dictionary)
        df = utils.process_time_series(series, time_data)

    return df
