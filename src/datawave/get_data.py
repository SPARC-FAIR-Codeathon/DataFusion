import os
import utils
import mat_file
import adicht_file
import rhd_file

def run(data_file_ext, data_file, field_name_dictionary):
    supported_ext = [".mat", ".nwb", ".csv", ".txt", ".adicht", ".rhd"]

    if data_file_ext == supported_ext[0]:
        series, time_data = mat_file.read_mat(data_file, field_name_dictionary)
        df = utils.process_time_series(series, time_data)

    ## Add linux implementation in future
    # if data_file_ext == supported_ext[4]: ## adicht
    #     series, time_data = adicht_file.read_adi_file(data_file, field_name_dictionary)
    #     df = utils.process_time_series(series, time_data)

    elif data_file_ext == supported_ext[5]: ## rhd
        df = rhd_file.run(data_file)


    return df
