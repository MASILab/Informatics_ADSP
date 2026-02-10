simg=/nfs2/harmonization/singularities/WMAtlas_v1.4.simg
datadir=/nfs/masi/kimm58/containerization_data/nondeterminism/EVE3

cmd="export OMP_NUM_THREADS=2; export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=2; bash /CODE/get_transforms.sh"

for i in {1..50}; do

    #bind for the template
    outdir=$datadir/iter_$i
    mkdir -p $outdir
    echo "singularity exec -B ${datadir}/inputs:/INPUTS -B $outdir:/OUTPUTS $simg bash -c \"$cmd\" > $outdir/log.txt" >> $datadir/cmds.txt
done