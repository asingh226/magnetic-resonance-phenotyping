# requires AjaybatchProcessingwithPandas.py
# import header from the pyradiomics helloPyradiomics notebook
from __future__ import print_function
import sys
import os


# imports added by Ajay for data processing, exploratory analysis, and statistics
import pandas as pd
import numpy as np

from python_functions.AjaybatchProcessingWithPandas import main as batchprocess

def main(full_image_directory, label, full_roi_mask_directory, imageType, roi, parameterPath):
    # define the path to directory containing the subjects to be processed
#     case_control = animalType
#     day = imageDay
    output_file_name = label
#     case_control_path = os.path.join(case_control, day)

    # create the paths to the images to be analyzed
    subjectPath = full_image_directory + '/'
    subjectFiles = os.listdir(subjectPath)

    #selects files in direcotry that are type '.nii.gz' only 
    imageFiles = [f for f in subjectFiles if '.nii.gz' in f]
    imagePath = [subjectPath+i for i in imageFiles]

    # create the paths to the roi masks to be analyzed
    roi  = roi
    roiPath = full_roi_mask_directory + '/' + roi +'/'
    if roi == 'full_brain_roi':   ### issue with size of the mask and image not being the same ### 
        roiPath = roiPath + case_control_path + '/'
    roiFiles = os.listdir(roiPath)

    if roi == 'full_brain_roi':
        maskPath = [roiPath + r for r in roiFiles]
    else: 
        maskPath = [roiPath + r for r in roiFiles] * len(imagePath) # odd way of determining length to do same ROI on every image

    #create a dataframe containing the filenames, imagepaths, and maskpaths 
    filePaths = {'filename':imageFiles, 'Image':imagePath, 'Mask':maskPath}
    fileDataFrame = pd.DataFrame(data=filePaths).set_index('filename')

    #create a .csv that can be used to allow batchprocess to find the image and mask files efficiently; saves in directory in which this is run
    fileDataFrame.to_csv('fileDataFrame.csv')

    # print names and first row to ensure that files pulled are the correct files for radiomics processing
    print(output_file_name)
    print(fileDataFrame.index)
    print(fileDataFrame.Image[0])
    print(fileDataFrame.Mask[0])

   
    # print('Parameter file, absolute path:', os.path.abspath(paramPath))
    # run batchprocess, produces .csv files of the radomics data; function more proprely defined in AjaybatchProcesssingWithPandas.py
    batchprocess('fileDataFrame.csv', output_file_name, roi ,imageType, output_file_name+'_log', parameterPath)