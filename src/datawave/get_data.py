import os
import utils
import mat_file
#import adicht_file
import pandas as pd

def run(data_file_ext, data_file, field_name_dictionary):
    """
    Covnerts the files to csv, nwb, h5 (wherever applicable)
    :param data_file_ext- extension of the input data files
    :param data_file- file name/path
    :param field_name_dictionary- field names as derived from json file
    :return pandas dataframe of the csv file
    """
    
    supported_ext = [".mat", ".nwb", ".csv", ".txt", ".adicht", ".rhd"]
    df = None
    if data_file_ext == supported_ext[0]:
        series, time_data = mat_file.read_mat(data_file, field_name_dictionary)
        if (series is not None) and (time_data is not None):
            df = utils.process_time_series(series, time_data)
            df = mat_file.add_other_labels(data_file, field_name_dictionary, df)
        else:
            df = pd.DataFrame({"Time": "empty", "Series": "empty" })

        mat_file.convert_mat_to_h5(data_file) 

    ## Add linux implementation in future
    # if data_file_ext == supported_ext[4]: ## adicht
    #     series, time_data = adicht_file.read_adi_file(data_file, field_name_dictionary)
    #     df = utils.process_time_series(series, time_data)

    elif data_file_ext == supported_ext[5]: ## rhd
        import rhd_file ## import only when the extension exists, because of dependencies issues
        df = rhd_file.run(data_file)
        rhd_file.rhd_to_nwb(data_file)

    elif data_file_ext == supported_ext[2]: ## csv
        df = pd.read_csv(data_file)

    return df
