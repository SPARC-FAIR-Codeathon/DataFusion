## created with help from- https://github.com/Intan-Technologies/load-rhd-notebook-python/tree/main
import importrhdutilities as rhdutils
import pandas as pd
import subprocess

class ChannelNotFoundError(Exception):
    pass


def channel_to_dataframe(channel_name, result):
    """Converts the data associated with the channel specified as 'channel_name'
    in the 'result' dict to a pandas DataFrame.
    """
    # Find channel that corresponds to this name
    channel_found, signal_type, signal_index = rhdutils.find_channel_in_header(
        channel_name, result)

    if channel_found:
        if signal_type == 'amplifier_channels':
            signal_data_name = 'amplifier_data'
            t_vector = result['t_amplifier']

        elif signal_type == 'aux_input_channels':
            signal_data_name = 'aux_input_data'
            t_vector = result['t_aux_input']

        elif signal_type == 'supply_voltage_channels':
            signal_data_name = 'supply_voltage_data'
            t_vector = result['t_supply_voltage']

        elif signal_type == 'board_adc_channels':
            signal_data_name = 'board_adc_data'
            t_vector = result['t_board_adc']

        elif signal_type == 'board_dig_in_channels':
            signal_data_name = 'board_dig_in_data'
            t_vector = result['t_dig']

        elif signal_type == 'board_dig_out_channels':
            signal_data_name = 'board_dig_out_data'
            t_vector = result['t_dig']

        else:
            raise ChannelNotFoundError(
                f"Conversion failed; signal type '{signal_type}' not found."
            )

        # Extract the signal data
        signal_data = result[signal_data_name][signal_index, :]

        # Create a DataFrame with the time vector as the index
        df = pd.DataFrame({"time": t_vector, channel_name: signal_data})

        return df

    else:
        raise ChannelNotFoundError(
            f"Conversion failed; channel '{channel_name}' not found."
        )


def run(filename):
    result, data_present = rhdutils.load_file(filename)

    df_list = []

    # Check if 'aux_input_channels' exists in result before processing
    if "aux_input_channels" in result.keys():
        for chan in result["aux_input_channels"]:
            df_list.append(channel_to_dataframe(chan["native_channel_name"], result))

    ## no implemented to save

    # # Check if 'amplifier_channels' exists in result before processing
    # if "amplifier_channels" in result.keys():
    #     for chan in result["amplifier_channels"]:
    #         df_list.append(channel_to_dataframe(chan["native_channel_name"], result))

    # # Check if 'supply_voltage_channels' exists in result before processing
    # if "supply_voltage_channels" in result.keys():
    #     for chan in result["supply_voltage_channels"]:
    #         df_list.append(channel_to_dataframe(chan["native_channel_name"], result))

    # # Check if 'board_adc_channels' exists in result before processing
    # if "board_adc_channels" in result.keys():
    #     for chan in result["board_adc_channels"]:
    #         df_list.append(channel_to_dataframe(chan["native_channel_name"], result))

    df = pd.concat(df_list)

## todo
def rhd_to_nwb (filename):
    repo_url = "https://github.com/Intan-Technologies/IntanToNWB.git"
    clone_dir = 'IntanToNWB'
    try:
        subprocess.run(['git', 'clone', repo_url, clone_dir], check=True)
    except subprocess.CalledProcessError as e:
        return None
