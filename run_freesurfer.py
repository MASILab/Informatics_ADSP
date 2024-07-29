import os
import sys
import subprocess
from multiprocessing import Pool, cpu_count
from pathlib import Path
import time

simg = "/nfs2/ForMichael/freesurfer_7.2.0.sif"
dir = "/fs5/p_masi/kimm58/Informatics/processing_test_local"
license = "/nfs2/harmonization/singularities/FreesurferLicense.txt"

def process_file(args):
    simg_path, root, license_file, t1 = args
    
    ses = Path(t1).parent.name

    #get the output directory
    out_dir = Path(root)/'outputs'/ses
    
    # Create output directory if it doesn't exist
    #os.makedirs(out_dir, exist_ok=True)

    # Prepare the command
    cmd = "time singularity exec -e --contain -B {}:/usr/local/freesurfer/.license -B {}:{} -B {}:{} {} recon-all -i {} -subjid freesurfer -sd {}/ -all > {}/freesurfer.log".format(license_file, t1, t1, out_dir, out_dir, simg_path, t1, out_dir, out_dir)
    
    # Run the command and capture output
    #print(f"Processing {index + 1}: {line} - Started")
    timein = time.time()
    subprocess.run(cmd, shell=True)
    #print(cmd)
    timeout = time.time()

    #print the time it took
    print(f"Processing {t1} took {timeout - timein} seconds")
    #print(f"Processing {index + 1}: {line} - Completed")


#using pathlib, find all the T1 files
t1_files = [x for x in (Path(dir)/'inputs').rglob('*.nii.gz')]

#with multiprocessing, process each T1 file
with Pool(cpu_count()) as p:
    p.map(process_file, [(simg, dir, license, str(t1)) for t1 in t1_files])




