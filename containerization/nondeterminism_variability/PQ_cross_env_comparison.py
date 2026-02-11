"""
50 runs on viselab
50 runs on masi-71
Comparing the variabilities
"""

from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nibabel as nib
import pandas as pd

root1 = Path("/nfs/masi/kimm58/containerization_data/nondeterminism/PreQual")
root2 = Path("/nfs/masi/kimm58/containerization_data/nondeterminism/PreQual/viselab")
root1_variability_dir = root1 / "variability"
root2_variability_dir = root2 / "variability"

#compare the median intensity histograms within the WM masks of the mean images?

mean1_file = root1_variability_dir / "mean_dwi.nii.gz"
mean2_file = root2_variability_dir / "mean_dwi.nii.gz"
fa_mask_1_file = root1_variability_dir / "fa_mask.nii.gz"
fa_mask_2_file = root2_variability_dir / "fa_mask.nii.gz"

mean1 = nib.load(mean1_file).get_fdata()
mean2 = nib.load(mean2_file).get_fdata()
fa_mask_1 = nib.load(fa_mask_1_file).get_fdata()
fa_mask_2 = nib.load(fa_mask_2_file).get_fdata()

#plot violin plots of every single volume masked
mean1_masked = mean1[fa_mask_1 > 0]
mean2_masked = mean2[fa_mask_2 > 0]
df_1 = pd.DataFrame(mean1_masked).melt(var_name='Volume', value_name='Intensity')
df_1['Machine'] = 'AMD EPYC 9534'
df_2 = pd.DataFrame(mean2_masked).melt(var_name='Volume', value_name='Intensity')
df_2['Machine'] = 'Intel(R) Xeon(R) Gold 6138 CPU'
df = pd.concat([df_1, df_2], ignore_index=True)

f,ax = plt.subplots(1,1, figsize=(12,6), constrained_layout=True)
sns.boxplot(x='Volume', y='Intensity', hue='Machine', data=df, showfliers=False, ax=ax)
f.suptitle("Comparison of Mean DWI Intensities within FA Mask")

f.savefig("mean_hist_comparison.png", bbox_inches='tight')