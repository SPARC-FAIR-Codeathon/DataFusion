import numpy as np
import pandas as pd

## params
num_neurons = 10
num_samples = 1000
time_end = 10  # seconds

# time stamps
timestamps = np.linspace(0, time_end, num_samples)

## LFP signals
np.random.seed(0)  
lfp_signals = np.array([np.sin(5 * np.pi * 1 * timestamps) + np.random.normal(0, 0.001, num_samples) for _ in range(num_neurons)]).T

## Generate labels 
labels = np.random.randint(0, 3, num_samples)

## Add noise based on behavioral labels
noise_dict = {0:0, 1: 0.5, 2: 1 }  # Adjust the magnitude of the noise as needed

## Create a copy of the original signals to modify
noisy_lfp_signals = lfp_signals.copy()

for label in np.unique(labels): 
    noise_magnitude = noise_dict[label]
    indices = np.where(labels == label)[0]
    noisy_lfp_signals[indices, :] += np.random.normal(0, noise_magnitude, (len(indices), num_neurons))

## save as a df
df = pd.DataFrame(noisy_lfp_signals, columns=[f'Neuron_{i+1}' for i in range(num_neurons)])
df['Label'] = labels

## Save to a CSV file 
df.to_csv('noisy_lfp_signals.csv', index=False)

