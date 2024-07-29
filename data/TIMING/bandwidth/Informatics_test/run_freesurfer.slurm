#!/bin/bash

#SBATCH --mail-user=michael.kim@vanderbilt.edu
#SBATCH --mail-type=FAIL
#SBATCH --nodes=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00
#SBATCH --array=1-6%6
#SBATCH --output=/nobackup/p_masi/kimm58/projects/Informatics_test/logs/logs_%A_%a.out

path='/nobackup/p_masi/kimm58/projects/Informatics_test/scripts/'
bash ${path}${SLURM_ARRAY_TASK_ID}.sh
