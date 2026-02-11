simg=/nfs2/harmonization/singularities/PreQual_v1.0.8.simg
datadir=/nfs/masi/kimm58/containerization_data/nondeterminism/PreQual

cmd="singularity run -ec -B /nfs2/harmonization/singularities/FreesurferLicense.txt:/APPS/freesurfer/license.txt -B /tmp:/tmp"
args="--topup_first_b0s_only --synb0 stripped"

for i in {1..50}; do

    #bind for the template
    outdir=$datadir/iter_$i
    mkdir -p $outdir
    echo "$cmd -B ${datadir}/inputs:/INPUTS -B $outdir:/OUTPUTS $simg j $args > $outdir/log.txt" >> $datadir/cmds.txt
done