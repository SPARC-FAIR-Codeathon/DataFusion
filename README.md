# DataFusion

**A versatile multi-purpose o<sup>2</sup>S<sup>2</sup>PARC service to convert different file formats (such as *.mat and *.rhd) to a common format and to run preliminary analysis on different input formats**

## Introduction
### Accessing Datasets on SPARC: Simplifying the Process
Accessing datasets on SPARC can be a daunting task due to the multitude of available file formats. The SPARC portal hosts an abundance of time-series datasets, such as EMG, EEG, ECG, urodynamics, manometry, and more. These datasets, besides being immensely useful for novel analysis or replciation, present an opportunity for the training of sequence prediction and generation models, such as transformers, MAMBA, and RKWV, which have seen immense success in large language modeling.
However, the accessibility of these datasets is a significant bottleneck in the research process. The various formats available, such as `.adicht`, `.rhd`, `.mat`, and others, require different libraries for any analysis.
To address this issue, we present a versatile cloud solution that can be deployed on SPARC's o<sup>2</sup>S<sup>2</sup>PARC platform. This solution provides users with a simple way to perform preliminary analysis on any time-series dataset of their choice.


## Solution
**DataFusion Service** is a versatile and scalable solution designed to convert various file formats into a common CSV format. It also supports the conversion of neuroscience datasets, such as Intan \*.rhd files, into the NWB (Neuroscience Without Borders) format. NWB is also built on the principles of FAIR (Findable, Accessible, Interoperable, and Reusable), empowering neuroscientists worldwide to perform analyses on datasets prepared by other laboratories.
Users can upload their preferred datasets or directly access them using PENSIEVE or a URL from SPARC datasets. These can be used in tandem with a file picker service. To further support users in performing preliminary analyses, such as training a neural network decoder or visualizing the dynamics of any variable as it evolves over time, users can upload a Python script along with the necessary requirements to run their code. This can be done for their original file or the converted \*.csv file (`pandas DataFrame`).
Finally, the outputs, including NWB, CSV, and analysis result files, are stored in an output folder available for download.

## How to use?
#### Service Deployment Instructions
The service is currently available as a Docker container. In the future, it can be uploaded directly to o<sup>2</sup>S<sup>2</sup>PARC, as it is built using `cookiecutter-osparc-service`. To use it, follow these steps:

1. **Clone the repository**
    ```bash
    $ git clone 
    $ cd 
    ```

2. **Build the Docker image**

    Run the following commands in your terminal:

    ```bash
    $ make build
    $ docker build -t data_fusion_img .
    ```

3. **Validate the Docker container**

    To ensure everything is working correctly, run:

    ```bash
    $ docker run --mount type=bind,source=./validation/input,target=/input --mount type=bind,source=./validation/output,target=/output data_fusion_img
    ```

    If this command runs without errors, the service is functioning correctly. Note that warnings may appear during this process; these are expected.

4. **Troubleshooting**

    If the command does not work, ensure that the Docker daemon is running. Else report issues.


#### How to run analysis code?
To run the analysis code effectively, follow these guidelines:

1. **Create a Directory**:
   Create a directory named `analysis_py` where you will place all necessary files.

2. **Include Dependencies**:
   If your analysis has non-trivial dependencies, include a `requirements_analysis.txt` file in the `analysis_py` directory. This file should list all the required Python packages.

**Please note that currently, this service supports the use of only `python3.9`. Ensure that your script and dependencies are compatible with Python 3.9 when using this service.**


3. **Prepare Your Analysis Script**:
   Include an `analysis.py` file in the `analysis_py` directory. Make sure to adhere to the provided template for the script. 
   
**Do not change the names of files, folders, or functions defined in the template file.**

4. **Data Files**:
   You can reference either the uploaded data file or its converted CSV version (read as a pandas DataFrame) in your analysis script.

5. **Analysis Capabilities**:
   You can perform a wide range of tasks, including plotting figures, training a network, and leveraging cloud computing for model execution. Possibilities are endless.

6. **CUDA Support**:
   Note that CUDA is currently supported and may be included in future updates.

Follow these steps, to run the analysis code and achieve the desired results.


## Demo files 
To show  various use case scenarios, we have created demo input and output files. After building the Docker image, you can run the following commands:

1. **For MAT file format**

    ```bash
    docker run --mount type=bind,source=./demos/input/MatDataset,target=/input --mount type=bind,source=./demos/output/MatDataset,target=/output docker_img
    ```

    This command converts MAT files to CSV and H5 formats (a precursor to NWB) and stores them in a zip folder. Note that it is important to provide a JSON file with field names along with the data file. Currently, the process requires this JSON file, but we believe that a smarter solution can be created in the future where field names might not be necessary. Additionally, you can include labels (e.g., for training a decoder or classifier) in the JSON file alongside the "Time Series" and "Time Stamps" fields.

2. **For RHD file format**

    ```bash
    docker run --mount type=bind,source=./demos/input/RhdDataset,target=/input --mount type=bind,source=./demos/output/RhdDataset,target=/output docker_img
    ```

    This command converts Intan RHD files (a neurophysiology format) to CSV and NWB formats. No JSON file is required for this conversion.

3. **For direct CSV format**

    ```bash
    docker run --mount type=bind,source=./demos/input/CsvDataset,target=/input --mount type=bind,source=./demos/output/CsvDataset,target=/output docker_img
    ```

    This command processes a toy dataset created using a Python script. It runs an analysis code on the CSV file to train a TensorFlow model and saves the results of 5-fold cross-validation as a CSV file and the model file for one of the folds as an H5 file in the zip output folder.



## Currently Supported Conversions
|Sr. No.| Input Formats |Output Formats|
|-------|-----------------|-------|
|1. | \*.mat | \*.h5 (\*.nwb), \*.csv|
|2. | \*.h5 | \*.nwb|
|3. | \*.rhd | \*.nwb, \*.csv|

**Note:** The `.adicht` file format is currently not supported due to limitations with Linux and the use of the `adi-reader`. However, the code files for this format have been added, and future support will require only a trivial development intervention.

Other file formats can be easily included in the current pipeline developed for the OSparc platform.


## Strengths and FAIR principle alignment
Strengthing the 


-   Bridging a gap in scientific collaboration
    
-   Large number of different formats are available either free and open source or proprietary
    
-   High degree of deviation in academia and industry from data collection to data storage
    
-   Standardizing the file format




```

## Workflow (Process) Description 

### Setting up Environment

#### Clone repository
Please clone or download the repository on your system. 

https://github.com/ITISFoundation/osparc-simcore.git

#### Operating System
We used two different operating systems, MAC and WSL-2 (Ubuntu 22.04) for the development.
MAC - We used to develop our plugin
WSL-2 (Ubuntu 22.04) - For creating a plug-in

<font color="red"> Pranjal! Operating System - We took leverage of multiple system
</font>








#### Testing
We have tested the use of this containerized service on MacOS. Testing for other know systems such as windows and ubuntu are not done yet. However, we expect it to run as usual elsewhere.   

#### 



## Any question or issue?

We would love to hear from you. Hence, please open an issue [here]() and our team will get back to you within 1 business working day.

We wish you to **Happy DataFusion**.
by Team DataFusion


