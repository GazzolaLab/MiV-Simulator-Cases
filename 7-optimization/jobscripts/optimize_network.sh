#!/bin/bash
#SBATCH -J CA1_optimize_network
#SBATCH -o ./results/CA1_optimize_network.%j.o
#SBATCH --nodes=86
#SBATCH --ntasks-per-node=53
#SBATCH -t 48:00:00
#SBATCH -p normal

cd "$(dirname "$0")/../Hippocampal-Dissociated-Culture"

module load phdf5
source $SCRATCH/venv/bin/activate
export PYTHONPATH=.:$PYTHONPATH

export I_MPI_ADJUST_SCATTER=2
export I_MPI_ADJUST_SCATTERV=2
export I_MPI_ADJUST_ALLGATHER=2
export I_MPI_ADJUST_ALLGATHERV=2
export I_MPI_ADJUST_ALLTOALL=4
export I_MPI_ADJUST_ALLTOALLV=2
export I_MPI_ADJUST_ALLREDUCE=6

export KERAS_BACKEND=torch
export DATA_PREFIX=$SCRATCH/data/MiV

results_path=$SCRATCH/results/CA1_optimize_network_$SLURM_JOB_ID
mkdir -p $results_path

ibrun -n 4558 \
    optimize-network \
    --config-path=../config/optimize_network.yaml \
    --optimize-file-dir=$results_path \
    --nprocs-per-worker=49 \
    --n-initial=3 \
    --n-epochs=5 \
    --initial-method=slh \
    --population-size=100 \
    --num-generations=100 \
    --resample-fraction=0.93 \
    --verbose \
    --no_cleanup \
    --dataset_prefix="$DATA_PREFIX" \
    --config_prefix=config \
    --results_path=$results_path \
    --mechanisms_path=mechanisms/build \
    --arena_id=A \
    --stimulus_id=Diag \
    --coordinates_namespace="Generated Coordinates" \
    --spike_input_path="${DATA_PREFIX}/Slice/CA1_Slice_100_dynamical_response_features_20250912.h5" \
    --spike_input_namespaces='Spatiotemporal Feature Spikes drc_features_20250912' \
    --spike_input_attr='Spike Train' \
    --max_walltime_hours=48 \
    --io_size=1
