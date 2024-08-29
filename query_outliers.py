import pandas as pd
import numpy as np
from tqdm import tqdm

def within_std_dev_range(value, mean, std_dev, num_std_devs):
    return mean - num_std_devs * std_dev <= value <= mean + num_std_devs * std_dev

def is_IQR_outlier(value, lower_bound, upper_bound):
    #return value < lower_bound or value > upper_bound
    return value > lower_bound and value < upper_bound

#for checking within a certain number of standard deviations
def check_stdev_range(bad_rows, df, means, stdevs, num_std_devs):
    results = {}
    for _,row in tqdm(bad_rows.iterrows()):
        close_to_mean = {}
        for column in [x for x in df.columns if x not in ['file', 'sub', 'ses', 'acq', 'run', 'key']]:
            value = row[column]
            if within_std_dev_range(value, means[column], stdevs[column], num_std_devs=num_std_devs):
                close_to_mean[column] = value
        results[row['file']] = close_to_mean
    return results

#for checking IQR
def check_IQR_outliers(bad_rows_df, df, lower_bound, upper_bound):
    results = {}
    for _, row in tqdm(bad_rows_df.iterrows(), total=bad_rows_df.shape[0]):
        close_to_mean = {}
        for column in [x for x in df.columns if x not in ['file', 'sub', 'ses', 'acq', 'run', 'key']]:
            value = row[column]
            if is_IQR_outlier(value, lower_bound[column], upper_bound[column]):
                close_to_mean[column] = value
        results[row['file']] = close_to_mean
    return results

df = pd.read_csv("/nfs2/kimm58/ADNI_TICV_volumes_BIDS.csv")

means = df.drop(columns=['file', 'sub', 'ses', 'acq', 'run']).mean()
stdevs = df.drop(columns=['file', 'sub', 'ses', 'acq', 'run']).std()
Q1 = df.drop(columns=['file', 'sub', 'ses', 'acq', 'run']).quantile(0.25)
Q3 = df.drop(columns=['file', 'sub', 'ses', 'acq', 'run']).quantile(0.75)
IQR = Q3 - Q1



#get the rows we want to check based on the QA csv
qc_df = pd.read_csv("/nfs2/harmonization/ADSP_QA/ADNI_DTI/SLANT-TICVv1.2/QA.csv")

#get the rows where QA_status is no
bad_rows = qc_df[qc_df['QA_status'] == 'no']

#print(bad_rows.shape)

#now, get the rows from the dataframe (sub,ses,acq,run) that match the bad rows
df['key'] = df['sub'] + '_' + df['ses'] + '_' + df['acq'] + '_' + df['run']
bad_rows['key'] = bad_rows['sub'] + '_' + bad_rows['ses'] + '_' + bad_rows['acq'] + '_' + bad_rows['run']

bad_rows_df = df[df['key'].isin(bad_rows['key'])]
bad_rows_df = bad_rows_df.drop(columns=['key', 'sub', 'ses', 'acq', 'run'])

#check several stdev ranges
for i in [0.5, 1, 2, 3]:
    results = check_stdev_range(bad_rows_df, df, means, stdevs, num_std_devs=i)
    results_df = pd.DataFrame(results).T
    results_df.to_csv('/home-local/kimm58/Informatics/simple_outlier_detection/ADNI_TICV_volumes_BIDS_stdev_{}_outliers.csv'.format(i))

#check IQR
for i in [0.5, 1.5, 3]:
    lower_bound = Q1 - i * IQR
    upper_bound = Q3 + i * IQR
    results = check_IQR_outliers(bad_rows_df, df, lower_bound, upper_bound)
    results_df = pd.DataFrame(results).T
    results_df.to_csv('/home-local/kimm58/Informatics/simple_outlier_detection/ADNI_TICV_volumes_BIDS_IQR_{}_outliers.csv'.format(i))



