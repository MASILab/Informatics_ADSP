arr=('masi-24' 'masi-26' 'GOAT' 'mastadon' 'MASI-64' 'masi-55' 'masi-43')

for machine in ${arr[@]}; do

logdir=/nfs/masi/kimm58/containerization_data/scripts_DLBS50/logs/${machine}_fsv7.2.0
mkdir $logdir
#ssh ${machine}.vuds.vanderbilt.edu "hostname"
#continue
#if [[ $(hostname) == "masi-24.vuds.vanderbilt.edu" ]]; then
	find /nfs/masi/kimm58/containerization_data/DLBS_50 -mindepth 4 -maxdepth 4 -type l -name "*T1w.nii.gz" | while IFS= read -r line; do
		sub=$(echo $line | awk -F '/' '{print $(NF-3)}')
		ses=$(echo $line | awk -F '/' '{print $(NF-2)}')
		fname=$(basename $line)
		if [[ $line == *"run-"* ]]; then
			run=$(echo $line | sed -E 's|^.*(run-.*)_.*$|_\1|g')
		else
			run=""
		fi
		outdir=/nfs/masi/kimm58/containerization_data/DLBS_50/derivatives/$sub/$ses/freesurfer7.2.0_${machine}${run}
		mkdir $outdir
		isdone=$(cat $outdir/freesurfer/scripts/recon-all.log | tail -n 20 | grep "finished without error")
		if [[ -z $isdone ]]; then
			echo "ssh ${machine}.vuds.vanderbilt.edu \"export OMP_NUM_THREADS=2; recon-all -i ${line} -subjid freesurfer -sd ${outdir} -all > ${logdir}/${fname}.log\"" >> run_cmds/${machine}_cmds.txt
		fi
	done
done

