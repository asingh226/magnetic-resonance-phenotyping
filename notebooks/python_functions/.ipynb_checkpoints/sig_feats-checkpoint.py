# ## by Vansh
# ##### function to compare two groups of animals (specific timept and case/control)
# ## function to pull radiomics data from csv and perform analysis (t-test, l2fc, multiple comparisons correction)
# ## outputs csv files and prints how many significant features

from __future__ import print_function

import os

# imports added by Ajay for data processing, exploratory analysis, and statistics
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.stats.multitest as multitest

def main(image, r, f, alpha, multipletest, timept1, animal1, timept2, animal2, save=False):
    
    ### lists of time points, ROIs, and feature classes
#     roi = ['full_brain', 'l_corpus_collosum', 'l_hippocampus', 'l_internal_capsule', 'r_amygdala', 'r_frontal_association_cortex', 'r_globus_pallidus', 'r_hippocampus']
#     feature_classes = ['firstorder', 'glcm', 'glszm', 'glrlm', 'gldm']
    
    path1 = timept1 + '_' + animal1
    path2 = timept2 + '_' + animal2
    compare_path = path1 + '_' + path2
        
    d_directory = os.path.join('..', 'results', 'results_VJ', image, r, 'comparisons', compare_path)
    if not os.path.exists(d_directory):
        os.makedirs(d_directory)

    maskROI = r
f
    ## pulls CSVs for specific time point and ROI and create data frames with info
    csv_name = (timept1 + '_' + animal1 + "_" + image+'.csv')
    csv_path = os.path.join('..', 'radiomics_data', image, r, csv_name)
    pre_a = pd.read_csv(csv_path).set_index('filename')

    csv_name = (timept2 + '_' + animal2 + '_'+ image+'.csv')
    csv_path = os.path.join('..', 'radiomics_data', image, r, csv_name)
    pre_b = pd.read_csv(csv_path).set_index('filename')


    # create data frame for data analysis
    l2fc_df = pd.DataFrame()

    # filter and create new data frames for specific feature class
    feature_class_reg = f
    a = pre_a.filter(regex=feature_class_reg)
    b = pre_b.filter(regex=feature_class_reg)

    #find the features that DO NOT have the exact same values for all replicates in both cases and controls
    cdif = (a.reset_index() != b.reset_index()).T.loc[:,0].drop('filename')

    #define a case and control dataset consisting only of differing features as defined above
    clean_a = a.T[cdif].T
    clean_b = b.T[cdif].T

    #find the mean for each feature for both cases and controls
    mean_a = clean_a.apply(np.mean,axis=0)
    mean_b = clean_b.apply(np.mean,axis=0)
    #calculate log 2 fold change (case/control) of all features
#     l2fc_mean_a_b = np.log2(mean_a/mean_b)

    ##create a label for the date of the animals and analyzed ROI
    #day = imageDay
    #date = [day]*len(mean_a)
    #roi_analyzed = [maskROI] *len(mean_a)

    #perform t-test on all features
    t_stat, p_val = stats.ttest_ind(clean_a,clean_b,axis=0)

    #perform FDR BH correction on t-test p-values; 
    # produces 4 values;: an array of booleans for rejecting null hypothesis, an array of corrected p_vals, 
    # the corrected alpha for Sidak Method, and corrected alpha for Bonferroni method
    reject_hypothesis, pvals_corrected, alphacSidak, alphacBonf = multitest.multipletests(p_val,alpha=alpha,method=multipletest)

    #Define columns in l2fc_df, make sure index for the dataframe is appropriate
    l2fc_df[path1] = mean_a
    l2fc_df[path2] = mean_b
#     l2fc_df['L2FC'] =l2fc_mean_a_b
    l2fc_df['p_val'] = p_val
    l2fc_df[multipletest+'_adjusted_p_val'] = pvals_corrected
    l2fc_df['roi'] = maskROI
    l2fc_df['day_1'] = timept1
    l2fc_df['animal_1'] = animal1
    l2fc_df['day_2'] = timept2
    l2fc_df['animal_2'] = animal2
    
    if save == True:

    #Create location to save file
        save_file_loc = os.path.join('..','results','results_VJ', image, maskROI,'sig_feats',compare_path,'_'.join([image,maskROI,f,'l2fc',compare_path, multipletest])+'.csv')
#        Save dataframe of mean scores, l2fc, pvalues, corrected pvalues to a .csv file; sort by fdr_adjusted_p_val
        l2fc_df.sort_values(multipletest+'_adjusted_p_val', ascending=True).to_csv(save_file_loc)
    
    #spot check to see if there are any significant features after FDR correction
#     print(f+'_'+maskROI+': There are ' + str(sum(reject_hypothesis)) +' significant features after ' +multipletest+' correction')
    return {'_'.join([f,r]): sum(reject_hypothesis)}

