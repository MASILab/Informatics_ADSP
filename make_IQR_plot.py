import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

column = 'Total_TICV'
range = 1.5

#read in the data
df = pd.read_csv("/nfs2/kimm58/ADNI_TICV_volumes_BIDS.csv")

#read in the outliers
outliers = pd.read_csv("/home-local/kimm58/Informatics/simple_outlier_detection/ADNI_TICV_volumes_BIDS_IQR_{}_outliers.csv".format(range))

#create a histogram of the Total_Brain_Volume
df[column] = df[column] / 1e6
plt.hist(df[column], bins=100)

#add the IQR ranges
Q1 = df[column].quantile(0.25)
Q3 = df[column].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
print("Lower bound: ", lower_bound)

plt.axvline(lower_bound, color='g', linestyle='--')
plt.axvline(upper_bound, color='purple', linestyle='--')

#now, also draw a small red line for each outlier
for _, row in outliers.iterrows():
    #for total brain volume
    #if row[0] not in ['sub-0821_ses-adni3screening_acq-MPRAGE_run-3_T1w_seg.nii.gz', 'sub-0166_ses-adni2year2_acq-MPRAGE_run-2_T1w_seg.nii.gz', 'sub-0257_ses-adni2year2_acq-MPRAGE_run-1_T1w_seg.nii.gz']:
    #    continue
    #for total ticv
    if row[0] not in ['sub-0981_ses-adni2baseline_acq-MPRAGE_run-1_T1w_seg.nii.gz', 'sub-5004_ses-adni3baseline_acq-MPRAGE_run-1_T1w_seg.nii.gz', 'sub-5138_ses-adni2month3_acq-MPRAGE_run-3_T1w_seg.nii.gz']:
        continue
    plt.axvline(row[column]/1e6, color='r', ymin=0, ymax=0.05)
    print(row[0])

#range x axis from 0.5 to 2
plt.xlim(0.5, 2)

if column == 'Total_TICV':
    colx = 'Total TICV Volume'
else:
    colx = column
plt.xlabel("{} (millions cubic mm)".format(colx), fontsize=14)
plt.ylabel("Counts", fontsize=14)

#show a legend for the IQR range
plt.legend(["Q1 - {}* IQR".format(range), "Q3 - {}* IQR".format(range)], fontsize=12)

#plt.show()

#save the plot
plt.savefig('/home-local/kimm58/Informatics/simple_outlier_detection/ADNI_TICV_{}_IRQ_{}_outliers.png'.format(column, range))