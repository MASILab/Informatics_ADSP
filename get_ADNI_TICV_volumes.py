import nibabel as nib
import numpy as np
from pathlib import Path
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import pandas  as pd

def get_volumes(file):
    """
    Given a TICV segmentation, return a dictionary volumes for each of the non-zero labels
    """

    img = nib.load(file)
    data = img.get_fdata()
    vox_header = img.header
    vox_size = vox_header.get_zooms()
    assert len(vox_size) == 3, "Not a 3D image"
    labels = np.unique(data)
    volumes = {'file': Path(file).name}
    for label in labels:
        if label == 0:
            continue
        #get the number of voxels
        num_voxels = np.sum(data == label)
        #from this, calculate the volume in mm
        volume = num_voxels * np.prod(vox_size)
        volumes[label_dic[label]] = volume
    
    return volumes


def get_TICV_dict():
    """
    Return a dictionary of label -> TICV region name
    """

    #read in the TICV labels file
    #ticv_labels = Path("/home-local/kimm58/Informatics/slant_ticv_orig_labels.txt")
    ticv_labels = Path("/nfs2/kimm58/slant_ticv_orig_labels.txt")

    #read using numpy
    labels = np.loadtxt(ticv_labels, dtype=str)

    label_dic = {}
    for label in labels:
        label_dic[int(label[0])] = label[1]

    return label_dic


#get the TICV mapping dictionary
label_dic = get_TICV_dict()

#get all the TICV files
adni = "/nfs2/harmonization/BIDS/ADNI_DTI/derivatives"
cmd = "find {} -mindepth 6 -maxdepth 6 \( -type l -o -type f \) -name '*seg.nii.gz'".format(adni)
files = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip().splitlines()

#get the volumes for each file
with Pool(processes=16) as pool:
    results = list(tqdm(pool.imap(get_volumes, files, chunksize=1), total=len(files))) 

#now, combine all the results into a single dataframe
df = pd.DataFrame(results)

#and save it
df.to_csv('/nfs2/kimm58/ADNI_TICV_volumes.csv', index=False)
