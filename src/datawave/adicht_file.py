import adi
import numpy as np

def process_adi_file(f):
    num_channels = len(f.channels)
    channel_id = []
    for i in range(num_channels):
        channel_id.append(f.channels[i].id)

    num_records = len(f.records)
    record_id = []
    for i in range(num_records):
        record_id.append(f.records[i].id)

    return channel_id, record_id, f


def get_channel_record_id(file_path, field_name_dictionary=None):
    f = adi.read_file(file_path)
    return process_adi_file(f)


def read_adi_file(data_file, field_name_dictionary= None):
    channel_id, record_id, f = get_channel_record_id(data_file)
    ts = []
    for idx_channel_id, c_id in enumerate(channel_id):
        for idx_record_id, r_id in enumerate(record_id):
            try:  ## despite some ids being present in the data, it is not able to rerieve data from those ids, such ids are ignored
                ts.append(f.channels[c_id - 1].get_data(r_id))  ## for now it is appending data for all records into one
            except:
                pass

    ## create pseudo time data
    time_data = np.arange(1, len(ts)+1)
    return ts, time_data



