import nibabel as nib
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

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

def create_png(b0data, b1000data, fa_mask, cov_means, cmap, outfile, imghd):
    #create the plt figure
    f, ax = plt.subplots(4,3,figsize=(10.5*0.75, 4*2), constrained_layout=True)
    
    b0_masked = np.where(fa_mask > 0, b0data, 0)
    b1000_masked = np.where(fa_mask > 0, b1000data, 0)

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
        b0_wm_slice = np.rot90(get_slice(b0_masked, dim, slice), k=1)
        b1000_wm_slice = np.rot90(get_slice(b1000_masked, dim, slice), k=1)
        #plot the slices
        ax[0,dim].imshow(img_slice, cmap=cmap, aspect=ratio, vmin=0, vmax=0.05)
        ax[0,dim].axis('off')
        ax[1,dim].imshow(b1000_slice, cmap=cmap, aspect=ratio, vmin=0, vmax=0.05)
        ax[1,dim].axis('off')
        #plot COV inside the fa mask
        ax[2,dim].imshow(b0_wm_slice, cmap=cmap, aspect=ratio, vmin=0, vmax=0.02)
        ax[2,dim].axis('off')
        ax[3,dim].imshow(b1000_wm_slice, cmap=cmap, aspect=ratio, vmin=0, vmax=0.02)
        ax[3,dim].axis('off')
        if dim == 2:
            #add the colorbar to the right of the last columns
            cbar1 = f.colorbar(ax[0,dim].images[0], ax=ax[0:2,dim])
            cbar1.set_label('COV', color='white')
            cbar1.ax.yaxis.set_tick_params(color='white', labelcolor='white') # Also makes ticks white

            cbar2 = f.colorbar(ax[2,dim].images[0], ax=ax[2:4,dim])
            cbar2.set_label('COV', color='white')
            cbar2.ax.yaxis.set_tick_params(color='white', labelcolor='white') # Also makes ticks white

    #add titles to the top row
    ax[0,1].set_title(f'b0 ({cov_means[0]*100:.4f}% avg)', color='white')
    ax[1,1].set_title(f'b1000 ({cov_means[1]*100:.4f}% avg)', color='white')
    ax[2,1].set_title(f'b0 - WM only ({cov_means[2]*100:.4f}% avg)', color='white')
    ax[3,1].set_title(f'b1000 - WM only ({cov_means[3]*100:.4f}% avg)', color='white')
    #make the png packground black
    f.patch.set_facecolor('black')
    #save the slices
    plt.savefig(outfile, bbox_inches='tight')
    plt.close('all')

root = Path("/nfs/masi/kimm58/containerization_data/nondeterminism/PreQual")
variability_dir = root / "variability"

#average COV across b1000 volumes
b0_cov_file = variability_dir / "b0_cov_dwi.nii.gz"
b1000_cov_file = variability_dir / "b1000_cov_dwi.nii.gz"
b0_cov = nib.load(b0_cov_file).get_fdata()
b1000_cov = nib.load(b1000_cov_file).get_fdata()
#fa mask
fa_mask_file = variability_dir / "fa_mask.nii.gz"
fa_mask = nib.load(fa_mask_file).get_fdata()

#print the avg COV for each, and then also the avg COV within the FA mask
print(f"Average COV for b0: {np.nanmean(b0_cov):.4f}")
print(f"Average COV for b1000: {np.nanmean(b1000_cov):.4f}")
print(f"Average COV for b0 within FA mask: {np.nanmean(b0_cov[fa_mask > 0]):.4f}")
print(f"Average COV for b1000 within FA mask: {np.nanmean(b1000_cov[fa_mask > 0]):.4f}")
b0_cov_mean = np.nanmean(b0_cov)
b1000_cov_mean = np.nanmean(b1000_cov)
b1_wm_cov_mean = np.nanmean(b0_cov[fa_mask > 0])
b1000_wm_cov_mean = np.nanmean(b1000_cov[fa_mask > 0])
cov_means = [b0_cov_mean, b1000_cov_mean, b1_wm_cov_mean, b1000_wm_cov_mean]

#create the 3D png of the masked COV with a colorbar of slice (54, 54, 29)
outpng = variability_dir / "masked_cov_dwi.png"
create_png(b0_cov, b1000_cov, fa_mask, cov_means, cmap='hot', outfile=outpng, imghd=nib.load(b0_cov_file).header)