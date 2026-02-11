import nibabel as nib
from pathlib import Path
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy import ndimage

def get_slice(img, dim, slicenum):
    if dim==0:
        return img[slicenum,:,:]
    elif dim==1:
        return img[:,slicenum,:]
    else:
        return img[:,:,slicenum]

def get_aspect_ratio(dim, vox_dim):
    if dim == 0:
        vox_ratio = vox_dim[2]/vox_dim[1]
    elif dim == 1:
        vox_ratio = vox_dim[2]/vox_dim[0]
    elif dim == 2:
        vox_ratio = vox_dim[1]/vox_dim[0]
    return vox_ratio

def create_png(b0data, b1000data, cmap, outfile, imghd):
    #create the plt figure
    f, ax = plt.subplots(2,3,figsize=(10.5/3*2, 8), constrained_layout=True)
    
    #loop through sag, coronal, axial slices
    for dim in range(3):
        #get the center slice
        slice=b0data.shape[dim]//2
        #get the aspect ratio for plotting purposes
        vox_dims = imghd.get_zooms()
        ratio = get_aspect_ratio(dim, vox_dims)
        #get the slices we want to show
        img_slice = np.rot90(get_slice(b0data, dim, slice), k=1)
        b1000_slice = np.rot90(get_slice(b1000data, dim, slice), k=1)
        #plot the slices
        ax[0,dim].imshow(img_slice, cmap='hot', aspect=ratio, vmin=0, vmax=0.05)
        ax[0,dim].axis('off')
        ax[1,dim].imshow(b1000_slice, cmap='hot', aspect=ratio, vmin=0, vmax=0.05)
        ax[1,dim].axis('off')
        if dim == 2:
            #add the colorbar to the right of the last columns
            cbar1 = f.colorbar(ax[0,dim].images[0], ax=ax[:,dim], fraction=0.046, pad=0.04, text='COV', text_kw={'color': 'white'})
            cbar2 = f.colorbar(ax[1,dim].images[0], ax=ax[:,dim], fraction=0.046, pad=0.04)

    #make the png packground black
    f.patch.set_facecolor('black')
    #save the slices
    plt.savefig(outfile, bbox_inches='tight')
    plt.close('all')

root = Path("/nfs/masi/kimm58/containerization_data/nondeterminism/PreQual")
dwis = [root/f"iter_{n}/PREPROCESSED/dwmri.nii.gz" for n in range(1, 51)]
variability_dir = root / "variability"

mean_file = variability_dir / "mean_dwi.nii.gz"
std_file = variability_dir / "std_dwi.nii.gz"

if not mean_file.exists() or not std_file.exists():
    print("Calculating mean and standard deviation across DWIs...")
    #stack = np.array([nib.load(f).get_fdata() for f in dwis])
    stack = np.array([nib.load(f).get_fdata() for f in tqdm(dwis, desc="Loading DWIs")])
    mean = np.mean(stack, axis=0)
    stdev = np.std(stack, axis=0)
    #save the images
    nib.save(nib.Nifti1Image(mean, affine=np.eye(4)), mean_file)
    nib.save(nib.Nifti1Image(stdev, affine=np.eye(4)), std_file)

else:
    print("Loading precomputed mean and standard deviation...")
    mean = nib.load(mean_file).get_fdata()
    stdev = nib.load(std_file).get_fdata()

#calculate the COV 
cov_file = variability_dir / "cov_dwi.nii.gz"
if not cov_file.exists():
    print("Calculating coefficient of variation (COV)...")
    cov = stdev / mean
    nib.save(nib.Nifti1Image(cov, affine=np.eye(4)), cov_file)
else:
    print("Loading precomputed COV...")
    cov = nib.load(cov_file).get_fdata()

#get the avg mask
masks = [root/f"iter_{n}/PREPROCESSED/mask.nii.gz" for n in range(1, 51)]
mask_img = variability_dir / "avg_mask.nii.gz"
if not mask_img.exists():
    print("Calculating average mask...")
    mask_stack = np.array([nib.load(f).get_fdata() for f in tqdm(masks, desc="Loading masks")])
    avg_mask = np.mean(mask_stack, axis=0)
    #threshold at 0.5 to get a binary mask
    avg_mask[avg_mask>=0.5] = 1
    avg_mask[avg_mask<0.5] = 0
    nib.save(nib.Nifti1Image(avg_mask, affine=np.eye(4)), mask_img)
else:
    print("Loading precomputed average mask...")
    avg_mask = nib.load(mask_img).get_fdata()

#mask the COV
masked_cov = variability_dir / "masked_cov_dwi.nii.gz"
if not masked_cov.exists():
    print("Applying average mask to COV...")
    masked_cov_data = cov * avg_mask[..., np.newaxis] #if stack.ndim == 5 else cov * avg_mask
    nib.save(nib.Nifti1Image(masked_cov_data, affine=np.eye(4)), masked_cov)
else:
    print("Loading precomputed masked COV...")
    masked_cov_data = nib.load(masked_cov).get_fdata()

#average COV across b1000 volumes
b0_cov_file = variability_dir / "b0_cov_dwi.nii.gz"
b1000_cov_file = variability_dir / "b1000_cov_dwi.nii.gz"
if not b0_cov_file.exists() or not b1000_cov_file.exists():
    print("Calculating average COV for b0 and b1000 volumes...")
    b0_cov = masked_cov_data[..., 0]
    b1000_cov = masked_cov_data[..., 1:].mean(axis=-1)
    nib.save(nib.Nifti1Image(b0_cov, affine=np.eye(4)), b0_cov_file)
    nib.save(nib.Nifti1Image(b1000_cov, affine=np.eye(4)), b1000_cov_file)
else:
    print("Loading precomputed average COV for b0 and b1000 volumes...")
    b0_cov = nib.load(b0_cov_file).get_fdata()
    b1000_cov = nib.load(b1000_cov_file).get_fdata()

#get a WM mask by averaging the FA across the 50 runs and thresholding at 0.2
fa_mask = variability_dir / "fa_mask.nii.gz"
if not fa_mask.exists():
    print("Calculating FA mask...")
    fa_files = [root/f"iter_{n}/SCALARS/dwmri_tensor_fa.nii.gz" for n in range(1, 51)]
    fa_stack = np.array([nib.load(f).get_fdata() for f in tqdm(fa_files, desc="Loading FA maps")])
    avg_fa = np.mean(fa_stack, axis=0)
    nib.save(nib.Nifti1Image(avg_fa, affine=np.eye(4)), variability_dir / "avg_fa.nii.gz")
    avg_fa[avg_fa>=0.45] = 1
    avg_fa[avg_fa<0.45] = 0
    #apply the average mask (eroded version)
    final_mask = avg_fa * ndimage.binary_erosion(avg_mask, iterations=2)
    nib.save(nib.Nifti1Image(final_mask, affine=np.eye(4)), fa_mask)
else:
    print("Loading precomputed FA mask...")
    avg_fa = nib.load(fa_mask).get_fdata()

# #create the 3D png of the masked COV with a colorbar of slice (54, 54, 29)
# outpng = variability_dir / "masked_cov_dwi.png"
# if not outpng.exists():
#     print("Creating PNG visualization of masked COV...")
# create_png(b0_cov, b1000_cov, cmap='hot', outfile=outpng, imghd=nib.load(b0_cov_file).header)

#number of unique outputs - all different
#stdev and mean of outputs 
#COV of outputs
#create a PNG of the COV
    #one row for b0
    #onre row for avg COV across b1000

#if the hickory output was within the error of the other outputs