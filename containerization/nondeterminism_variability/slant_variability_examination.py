import nibabel as nib
import numpy as np
import hashlib
import gzip
from pathlib import Path

root = Path("/nfs/masi/kimm58/containerization_data/nondeterminism/SLANT")
t1 = root / "./iter_15/post/FinalResult/sub-ID1000x0001_run-1_T1w_seg.nii.gz"
t2 = root / "./iter_2/post/FinalResult/sub-ID1000x0001_run-1_T1w_seg.nii.gz"

def analyze_nifti_diff(file1, file2):
    img1 = nib.load(file1)
    img2 = nib.load(file2)
    
    print(f"--- Comparing {file1.parent.name} vs {file2.parent.name} ---")
    
    # 1. Check Raw Header Fields
    header1 = img1.header
    header2 = img2.header
    header_diffs = []
    
    for key in header1.keys():
        if not np.array_equal(header1[key], header2[key]):
            header_diffs.append((key, header1[key], header2[key]))
    
    if header_diffs:
        print("\n[!] Header Differences Found:")
        for key, v1, v2 in header_diffs:
            print(f"    Field '{key}':\n      Value 1: {v1}\n      Value 2: {v2}")
    else:
        print("\n[✓] Headers are identical.")

    # 2. Check Pixel Data (Array Content)
    data1 = img1.get_fdata()
    data2 = img2.get_fdata()
    
    if np.array_equal(data1, data2):
        print("[✓] Pixel data is identical.")
    else:
        max_diff = np.max(np.abs(data1 - data2))
        print(f"[!] Pixel data differs! Max Intensity Diff: {max_diff}")

    # 3. Check Gzip Metadata (Timestamp)
    with gzip.open(file1, 'rb') as f1, gzip.open(file2, 'rb') as f2:
        # The Gzip header is the first 10 bytes. Byte 4-7 is the MTIME (timestamp).
        f1.seek(0); f2.seek(0)
        gz_header1 = f1.myfileobj.read(10) # Access underlying file object
        f2.myfileobj.seek(0)
        gz_header2 = f2.myfileobj.read(10)
        
        if gz_header1 != gz_header2:
            print("\n[!] Gzip Compression Metadata Differs (Likely Timestamps):")
            print(f"    GZ Header 1: {gz_header1.hex()}")
            print(f"    GZ Header 2: {gz_header2.hex()}")

analyze_nifti_diff(t1, t2)