# DataFusion
**An o<sup>2</sup>S<sup>2</sup>PARC service to enhance the usability of SPARC by converting multiple SPARC’s public dataset file formats (or others) (such as \*.mat and \*.rhd) to a common format (\*.nwb) and facilitating hypothesis-driven studies by allowing preliminary analyses.**


### Dataset & Study Design Problems
In neuroscience, a large number of different data file formats are available that contain a high degree of deviation in datasets from data collection to data storage and thus, difficult for results’ reproducibility. This also leads to weak or no scientific collaborations at all. Moreover, due to the lack of access to the required resources, it is also very challenging to choose and use publically available datasets. Furthermore, various formats available, such as  `.rhd`, `.mat`, and others, require different libraries for any analysis.

### Motivation Behind DataFusion
DataFusion has been developed to bridge the gap among the stakeholders of neuroscience by utilizing Findable, accessible, interoperable, and reusable (FAIR) data principles and the common standardized file format - neurodata without borders (NWB). DataFusion also promotes hypothesis-driven studies to SPARC’s users who can choose the right dataset for their study by harnessing the potential of our preliminary analyses pipeline.

### Simplifying the Process to Access Datasets on SPARC 
Specific to Stimulating Peripheral Activity to Relieve Conditions (SPARC), accessing datasets can be a daunting task due to the multitude of available file formats. The SPARC portal hosts an abundance of time-series datasets, such as electroencephalography (EEG), electrocardiography (ECG), electromyography (EMG), urodynamics, manometry, and more. However, the accessibility of these datasets is a significant bottleneck in the research process. The various formats available, such as  `.rhd`, `.mat`, and others, require different libraries for any analysis.
To address this issue, we present a multi-purpose cloud solution that can be deployed on o<sup>2</sup>S<sup>2</sup>PARC platform. This solution provides users with a simple way to perform preliminary analysis on any time-series dataset of their choice.

## DataFusion - A Solution
We developed a service consisting of two functionalities that can either be used separately or together 
1. Conversion of different formats to a common format (\*.nwb)
2. Executing user-defined preliminary analyses
   
**DataFusion Service** is a versatile and scalable solution designed to convert various file formats into a common CSV format. CSV is a human-readable file unlike other file formats occasionally used to store time series data, enabling almost everybody (especially those who don't know how to code) to see the data quickly and if required use it to plot with Excel or Google Sheets. It also supports the conversion of neuroscience datasets, such as Intan \*.rhd files, into the NWB (Neuroscience Without Borders) format. NWB is also built on the principles of FAIR, empowering neuroscientists worldwide to perform analyses on datasets prepared by other laboratories.
Users can upload their preferred datasets or directly access them using PENSIEVE or a URL from SPARC datasets. These can be used in tandem with a file picker service. To further support users in performing preliminary analyses, such as training a neural network decoder or visualizing the dynamics of any variable as it evolves with time, users can upload a Python script along with the necessary requirements to run their code. This can be done for their original file or the converted \*.csv file (`pandas DataFrame`).
Finally, the outputs, including NWB, CSV, and analysis result files, are stored in an output folder available for download.

## How to use?
#### DataFusion Deployment - A step-by-step guidelines
The service is currently available as a Docker container. In the future, it can be uploaded directly to o<sup>2</sup>S<sup>2</sup>PARC, as it is built using `cookiecutter-osparc-service`. To use it, follow these steps:

1. **Clone the repository**
    ```bash
    $ git clone https://github.com/SPARC-FAIR-Codeathon/DataFusion.git
    $ cd DataFusion
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

4. **Input your files or run demos**
   
   To run demos refer to [this](#Demo-files). To run your/user-defined input files, use the following command after building the image. Add your filepaths in the defined placeholder.
   
    ```bash
    $ docker run --mount type=bind,source=<input_file_path>,target=/input --mount type=bind,source=<output_file_path>,target=/output data_fusion_img
    ```
    
6. **Troubleshooting**

    If the command does not work, ensure that the Docker daemon is running. Else report issues.



#### How to run analysis code?
To run the analysis code effectively, follow these guidelines (refer to [the third implementation in demos](#demo-files) to run user-defined analysis files):

1. **Create a Directory**:
   Create a directory named `analysis_py` where you will place all necessary files.

2. **Include Dependencies**:
   If your analysis has non-trivial dependencies, include a `requirements_analysis.txt` file in the `analysis_py` directory. This file should list all the required Python packages.

**Please note that currently, this service supports the use of only `python3.9`. Ensure that your script and dependencies are compatible with Python 3.9 when using this service.**

3. **Prepare Your Analysis Script**:
   Include an `analysis.py` file in the `analysis_py` directory. Make sure to adhere to the provided [template](https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/misc/template.py) for the script. Don't forget to rename the template to `analysis.py`.
   
**Do not change the names of files, folders, or functions defined in the template file.**

4. **Data Files**:
   You can reference either the uploaded data file or its converted CSV version (read as a pandas DataFrame) in your analysis script.

5. **Analysis Capabilities**:
   You can perform a wide range of tasks, including plotting figures, training a network, and leveraging cloud computing for model inference. The possibilities are endless.

6. **CUDA Support**:
   Note that CUDA is currently supported and may be included in future updates.

Follow these steps, to run the analysis code and achieve the desired results.


## Demo files 
To show  various use case scenarios, we have created demo input and output files. To use demo commands, download the [demos](https://drive.google.com/drive/folders/1SuU7rR7E7a27oN3rO2_Ob6GTzeBv8L-c?usp=drive_link) files (from team drive folder) and add it to DataFusion directory. After building the Docker image, you can run the following commands:

1. **For MAT file format**

    ```bash
    docker run --mount type=bind,source=./demos/input/MatDataset,target=/input --mount type=bind,source=./demos/output/MatDataset,target=/output docker_img
    ```

    This command converts MAT files (accessed from SPARC Dataset [375](https://sparc.science/datasets/375?type=dataset&datasetDetailsTab=about&path=files/primary/sub-DP8/perf-DP8-random-patterns) to CSV and H5 formats (a precursor to NWB) and stores them in a zip folder. Note that it is important to provide a JSON file with field names along with the data file. Currently, the process requires this JSON file, but we believe that a smarter solution can be created in the future where field names might not be necessary. Additionally, you can include labels (e.g., for training a decoder or classifier) in the JSON file alongside the "Time Series" and "Time Stamps" fields.

2. **For RHD file format**

    ```bash
    docker run --mount type=bind,source=./demos/input/RhdDataset,target=/input --mount type=bind,source=./demos/output/RhdDataset,target=/output docker_img
    ```

    This command converts Intan RHD files (a neurophysiology format) (accessed from SPARC Dataset [316](https://sparc.science/datasets/316?type=dataset&datasetDetailsTab=files&path=files/primary/sub-VN010720/perf-01-09-20-baseline) to CSV and NWB formats. No JSON file is required for this conversion.

3. **For direct CSV format**

    ```bash
    docker run --mount type=bind,source=./demos/input/CsvDataset,target=/input --mount type=bind,source=./demos/output/CsvDataset,target=/output docker_img
    ```

    This command processes a toy dataset created using a Python script. It runs an analysis code on the CSV file to train a TensorFlow model and saves the results of the 5-fold cross-validation as a CSV file and the model file for one of the folds as an H5 file in the zip output folder.

____
## Currently Supported Conversions

| Sr. No. | Input Formats | Output Formats | Dataset Reference |
|---------|---------------|----------------|-------------------|
| 1       | \*.mat        | \*.h5 (\*.nwb) & \*.csv | [375](https://sparc.science/datasets/375?type=dataset&datasetDetailsTab=about&path=files/primary/sub-DP8/perf-DP8-random-patterns) |
| 2       | \*.rhd        | \*.nwb & \*.csv | [316](https://sparc.science/datasets/316?type=dataset&datasetDetailsTab=files&path=files/primary/sub-VN010720/perf-01-09-20-baseline) |


**Note:** 
- The `.adicht` file format is currently not supported due to limitations with Linux and the use of the `adi-reader`. However, the code files for this format have been added, and future support will require only a trivial development intervention. 
- Other file formats can be easily included in the current pipeline developed for the OSparc platform.
- Currently \*.mat is being converted to \*.h5. Conversion to \*.nwb requires a trivial solution. [See this](https://github.com/NeurodataWithoutBorders/helpdesk/discussions/89) as discussed by [Muhammad Farhan Khalid](https://github.com/imeMFK01).

## Production and Process
Steps followed in the production process- 
1. Steps mentioned on [cookiecutter-osparc-service](https://github.com/ITISFoundation/cookiecutter-osparc-service) repository to create a pre-configured oSPARC service template were followed.
2. [Dockerfile](https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/docker/python/Dockerfile) and [metadata](https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/.osparc/metadata.yml) were configured to create the image and for seamless integration with osparc.
3.  [execute.sh](https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/service.cli/execute.sh) was developed to run custom defined python scripts.
4.  Custom Python scripts to do the conversion and run the user-defined analysis file was added to [src](https://github.com/SPARC-FAIR-Codeathon/DataFusion/tree/main/src).
5.  To validate and test the usability, example input and output files were added to [validation](https://github.com/SPARC-FAIR-Codeathon/DataFusion/tree/main/validation)
6.  A summary of the backend Python scripts is given [here](https://github.com/SPARC-FAIR-Codeathon/DataFusion/tree/main/src/datawave#readme).

## Testing
Only the MAC operating system has been tested for local DataFusion deployment.

## Strengths and FAIR principle alignment
The cornerstone of Findable, accessible, interoperable, and reusable (FAIR) is the ["reuse of scholarly data"](https://www.nature.com/articles/sdata201618) which is the primary objective of this service. By converting the available dataset to a common format (\*.nwb for neuroscience datasets and \*.csv for all time series data), we are necessarily aiming to empower scientists, scholars, students and researchers worldwide to reuse the existing data in an easy manner. Furthermore, FAIR wants to empower ["machines to automatically find and use the data"](https://www.nature.com/articles/sdata201618) which aligns perfectly with our solution. With a step forward, we also enable users to run their analysis files based on these datasets, further enabling them to make novel discoveries or replicate existing results!

## Reporting Issues or Contributions
We are delighted to have your kind input (such as reporting issues or suggestions for new features) for improving this repository. However, please review the existing issues before submitting a new one [here](https://github.com/SPARC-FAIR-Codeathon/DataFusion/issues). 

___
## Contributions
Everyone is welcome to contribute to this repository by using [pull requests](https://github.com/SPARC-FAIR-Codeathon/DataFusion/pulls). After reviewing your code we will merge with a main branch.

___
## License
This repository is based on the MIT License and further details can be found [here](https://github.com/SPARC-FAIR-Codeathon/DataFusion/blob/main/LICENSE)

___
## Any questions?
We would love to hear from you. Hence, please open an issue [here](https://github.com/SPARC-FAIR-Codeathon/DataFusion/issues) (as a discussion forum is not currently being supported in this repository) and our team will get back to you on this.

We wish you to **Happy DataFusioning**

by **Team DataFusion**


## Team Members*
- [Muhammad Farhan Khalid](https://github.com/imeMFK01)
- [Pranjal Garg](https://github.com/neurogarg)

_* team members are equally contributed_


