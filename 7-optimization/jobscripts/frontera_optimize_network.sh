#!/bin/bash
#SBATCH -J MiV_optimize_network_test
#SBATCH -o ./results/MiV_optimize_network_test.%j.o
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

export DATA_PREFIX=$SCRATCH/striped2/MiV
export CONFIG_PREFIX="config"

results_path=$DATA_PREFIX/results/optimize_network_$SLURM_JOB_ID
export results_path

mkdir -p ${results_path}

ibrun -n 9 \
    optimize-network \
    --config-path=./config/optimize_network.yaml \
    --optimize-file-dir=results/network \
    --verbose \
    --nprocs-per-worker=8 \
    --n-iter=1 \
    --num-generations=200 \
    --no_cleanup \
    --dataset_prefix="$DATA_PREFIX" \
    --config_prefix="$CONFIG_PREFIX" \
    --results_path=$results_path \
    --results-path=results/network \
    --spike_input_path="$DATA_PREFIX/Microcircuit_Small/Microcircuit_Small_input_spikes.h5" \
    --spike_input_namespace='Input Spikes' \
    --spike_input_attr='Spike Train' \
    --io_size=1 \
    --verbose
