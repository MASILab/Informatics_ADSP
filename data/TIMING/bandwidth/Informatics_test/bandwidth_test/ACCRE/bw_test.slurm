#!/bin/bash

#SBATCH --mail-user=michael.kim@vanderbilt.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --array=1-100%1
#SBATCH --output=/nobackup/p_masi/kimm58/projects/Informatics_test/bandwidth_test/logs/logs_%A_%a.out

path='/nobackup/p_masi/kimm58/projects/Informatics_test/bandwidth_test/scripts/'
bash ${path}${SLURM_ARRAY_TASK_ID}.sh ${SLURM_ARRAY_TASK_ID}
