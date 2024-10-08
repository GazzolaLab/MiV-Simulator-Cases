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

export CONFIG_PREFIX="config"

export DATA_PREFIX="/tmp/MiV_optimize_network"
export CDTools=/home1/apps/CDTools/1.2

export PATH=${CDTools}/bin:$PATH

results_path=$SCRATCH/results/optimize_network_$SLURM_JOB_ID
export results_path

mkdir -p ${results_path}

distribute.bash ${SCRATCH}/striped2/MiV/MiV_optimize_network

ibrun -n 28 \
    optimize-network \
    --config-path=./config/optimize_network.yaml \
    --optimize-file-dir=results/network \
    --verbose \
    --nprocs-per-worker=27 \
    --n-epochs=3 \
    --population-size=400 \
    --num-generations=200 \
    --initial-method='slh' \
    --no_cleanup \
    --dataset_prefix="$DATA_PREFIX" \
    --config_prefix="$CONFIG_PREFIX" \
    --results_path=$results_path \
    --arena_id=A \
    --stimulus_id=Diag \
    --coordinates_namespace="Coordinates" \
    --max_walltime_hours=2 \
    --io_size=1 \
    --verbose
