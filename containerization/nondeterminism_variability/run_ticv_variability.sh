simg=/nfs2/harmonization/singularities/nssSLANT_v1.2.simg
datadir=/nfs/masi/kimm58/containerization_data/nondeterminism/SLANT

cmd="singularity exec -ec"

for i in {1..50}; do

    #bind for the template
    outdir=$datadir/iter_$i
    mkdir -p $outdir/{pre,post,dl}
    indir=${datadir}/inputs
    binds="-B $indir:/opt/slant/matlab/input_pre -B $indir:/opt/slant/matlab/input_post -B $outdir/pre:/opt/slant/matlab/output_pre -B $outdir/post:/opt/slant/matlab/output_post -B $outdir/dl:/opt/slant/dl/working_dir"
    binds2="-B /tmp:/tmp --home $indir -B $indir/empty.sh:/${indir}/.bashrc"
    echo "$cmd $binds $binds2 $simg /opt/slant/run.sh > $outdir/log.txt" >> $datadir/cmds.txt
done