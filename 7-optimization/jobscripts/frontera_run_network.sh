#!/bin/bash
#SBATCH -J MiV_run_network
#SBATCH -o ./results/MiV_run_network.%j.o
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=56
#SBATCH -t 2:00:00
#SBATCH -p development      # Queue (partition) name
#SBATCH --mail-user=ivan.g.raikov@gmail.com
#SBATCH --mail-type=END
#SBATCH --mail-type=BEGIN
#

module load phdf5

export NEURONROOT=$SCRATCH/bin/nrnpython3_intel19
export PYTHONPATH=$HOME/model:$NEURONROOT/lib/python:$SCRATCH/site-packages/python3.10:$PYTHONPATH
export PATH=$NEURONROOT/bin:$SCRATCH/site-packages/python3.10/bin:$PATH

export I_MPI_ADJUST_SCATTER=2
export I_MPI_ADJUST_SCATTERV=2
export I_MPI_ADJUST_ALLGATHER=2
export I_MPI_ADJUST_ALLGATHERV=2
export I_MPI_ADJUST_ALLTOALL=4
export I_MPI_ADJUST_ALLTOALLV=2
export I_MPI_ADJUST_ALLREDUCE=6

export CONFIG_PREFIX="config"
export DATA_PREFIX="${SCRATCH}/striped2/MiV"

results_path=$SCRATCH/results/MiV_Microcircuit_Small_$SLURM_JOB_ID
export results_path

mkdir -p ${results_path}


ibrun run-network \
    --config-file=Network_Clamp_Microcircuit_Small_Tomko_PR.yaml  \
    --config-prefix="$CONFIG_PREFIX" \
    --arena-id=A \
    --stimulus-id=Diag \
    --coordinates-namespace="Coordinates" \
    --template-paths=templates \
    --dataset-prefix="$DATA_PREFIX" \
    --results-path=results \
    --io-size=1 \
    --tstop=2500 \
    --v-init=-75 \
    --results-write-time=60 \
    --stimulus-onset=0.0 \
    --max-walltime-hours=2.0 \
    --dt 0.025 \
    --verbose
