import numpy as np
import pandas as pd
import warnings


def process_time_series(series, time_data):
    time_data = time_data.flatten()
    # Check if the series is 3-dimensional
    if series.ndim == 3:
        warnings.warn("The series is 3-dimensional, which is not supported. Please check your data.")
        return None

    # If 2-dimensional and one of the dimensions is 1, reduce it to 1 dimension
    if series.ndim == 2:
        if series.shape[0] == 1 or series.shape[1] == 1:
            series = series.flatten()

    # If the series is 2-dimensional and both dimensions are greater than 1
    if series.ndim == 2:
        if series.shape[0] > 1 and series.shape[1] > 1:
            # Align the series with the time data
            if len(time_data) == series.shape[0]:
                df = pd.DataFrame(series, columns=[f'Series_{i + 1}' for i in range(series.shape[1])])
                df.insert(0, 'Time', time_data)


            elif len(time_data) == series.shape[1]:
                series = series.T
                df = pd.DataFrame(series, columns=[f'Series_{i + 1}' for i in range(series.shape[1])])
                df.insert(0, 'Time', time_data)

            else:
                raise ValueError("Length of time data and series does not match.")

    # If the series is 1-dimensional, simply align it with the time data
    if series.ndim == 1:
        if len(series) == len(time_data):
            df = pd.DataFrame(data={'Time': time_data, 'Series': series})
        else:
            raise ValueError("Length of time data and series does not match.")
    return df

# # Toy data
# time_data = np.arange(0, 10, 1).T  # Time from 0 to 9
# series_1d = np.sin(time_data)  # 1D time series data (sin wave)
# series_2d = np.array([np.sin(time_data), np.cos(time_data)])  # 2D time series data (sin and cos waves)

# # Process the 1D time series
# print("Processing 1D time series:")
# a = process_time_series(series_1d, time_data)

# # Process the 2D time series
# print("\nProcessing 2D time series:")
# b= process_time_series(series_2d, time_data)