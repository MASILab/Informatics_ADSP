
if [[ -z $1 || -z $2 || -z $3 ]]; then
    echo "Usage: $0 <simg_path> <root_path> <license_file>"
    exit 1
fi

#find the inputs
simg_path=$(readlink -f $1)
root=$(readlink -f $2)
license=$(readlink -f $3)

i=0
find $root/inputs -name "*T1w.nii.gz" | while IFS= read -r line
do
    i=$((i+1))
    #echo "Processing $i: $line"
    #get the session
    ses=$(dirname $line)

    #get the output directory
    out_dir=$root/outputs/$(basename $ses)
    echo $out_dir

    #now, run freesurfer
    echo "time singularity exec -e --contain -B $license:/usr/local/freesurfer/.license -B $line:$line -B $out_dir:$out_dir $simg_path recon-all -i $line -subjid freesurfer -sd $out_dir/ -all > $out_dir/freesurfer.log" > /panfs/accrepfs.vampire/nobackup/p_masi/kimm58/projects/Informatics_test/scripts/${i}.sh

done