# Magnetic Resonance Phenotyping (MRP)

This repository contains all the code and files needed to run an MRP analysis on several rat models of altered neurodevelopment (_Disc1, Nrxn1, Pten, Fmr1_). All images used here are NODDI (**N**eurite **O**rientation **D**ispersion and **D**ensity **I**maging) images. NODDI is a microstructural modelling approach for diffusion MRI data [Zhang *et al.*, NeuroImage 2012]. 

Below is a description of directories and files in the repository, its contents, and its role in the pipeline.

**Repository layout**
- [images](#images)
- [notebooks](#notebooks)
  - [Radiomics Processing.ipynb](#radiomics-processing.ipynb)
  - [MRP Analysis Pipeline.ipynb](#mrp-analysis-pipeline.ipynb)
  - [python_functions](#python_functions)
- [radiomics_data_control + radiomics_data_nrxn](#radiomics_data_control-+-radiomics_data_nrxn)
- [radiomics_features_list](#radiomics_features_list)
- [requirements](#requirements)
- [results](#results)
- [roi](#roi)
- [Dockerfile_MRP](#Dockerfile_MRP)

## images

This directory contains all NODDI images divided by the NODDI compartment image type (vISO, NDI, ODI). The images are further organized by experimental design (e.g. sex, age, genotype, etc.)

## notebooks
This directory contains the sub-directory 'python_functions' and two Jupyter notebooks: "Radiomics Processing.ipynb" and "MRP Analysis Pipeline.ipynb" 

### Radiomics Processing.ipynb
This notebook contains the function used to create the necessary directories to organize the radiomics processing of images and the function to process batches of images. In-line comments describe each functoin and its use in detail. There is also an example processing run. 
- **create_directories**: creates directories to set-up the directory structure for radiomics processing and MRP analysis
- **imageBatchProcess**: function to perform iterative batch radiomics processing

### MRP Analysis Pipeline.ipynb
This notebook contains the functions to run a magnetic resonsance analysis and visualization and in-line comments describing each function and its use in detail. It also has an example analysis of the _Nrxn_ data. Below is a list of the functions and a brief description:
- **two_groups_feature_analysis_byclass**: compares and tests the mean difference for each radiomic feature between two datasets; calculates log 2 fold change
- **feature_table**: converts the output of two_groups_feature_analysis_byclass into a convenient table for downstream anlaysis and visualization
- **feature_heatmap**: uses feature_table output to produce MRP heatmap signatures
- **feature_jaccard_score**: uses feature_table outputs to calculate Jaccard similarity index for MRP signatures
- **volcanoPlot**: uses feature_table output to generate volcano plot of MRP signatures

### python_functions
This sub-directory contains an "__ init__.py" to enable function importing from this directory and  "YuLabbatchProcessingWithPandas.py" which is a python file adapted and modified from the original PyRadiomics pipeline and contains a function that will be used in "Radiomics Processing.ipynb"

## parameters
This directory contains all the .yaml parameter files used for the radiomics processing. The difference between all the parameter files listed in this directory is the bin width used for gray level discretization. 

## radiomics_data_control + radiomics_data_nrxn
These directories contain the processed radiomics data for the control and _Nrxn_ animals respectively. They are organized by parameter type, image type, and region of interest. The PyRadiomics output is saved in a subdirectory 'PyRadiomics_raw_data.' The log-two fold change between _Nrxn_ and control animals is saved in a subdirectory called 'comparisons' within the 'radiomics_data_nrxn' region of interest sub-directories.

## radiomics_features_list 
This directory holds a .csv file containing the names of all radiomic features that can be analyzed. This .csv file is used when generating the MRP signature in the MRP analysis pipeline. 

## results
This directory contains results from the MRP analysis and is organized by experiment and visualization type. 

## requirements
This directory contains all the set-up requirements for the Docker environment used to run the python pipelines. This also includes set-up requirements from the PyRadiomics library which is found in the sub-directory 'radiomics'

## roi
This directory contains sub-directories for each region of interest. Within those sub-directories are the image masks used to segement the regions of interest during the radiomics image processing. 

## Dockerfile_MRP
This is the Docker build for the Docker environment created for this processing and analysis. 


