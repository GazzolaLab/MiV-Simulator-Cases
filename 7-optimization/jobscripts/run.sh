#!/bin/bash
#SBATCH -J CA1_run_network
#SBATCH -o ./results/CA1_run_network.%j.o
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=56
#SBATCH -t 4:00:00
#SBATCH -p normal

cd "$(dirname "$0")/../Hippocampal-Dissociated-Culture"

module load phdf5
source $SCRATCH/venv/bin/activate
export PYTHONPATH=.:$PYTHONPATH
export DATA_PREFIX=$SCRATCH/data/MiV

results_path=$SCRATCH/results/CA1_run_network_$SLURM_JOB_ID
mkdir -p $results_path

ibrun run-network \
    --config-file=Slice_Tuned_Joint_Surrogate_Oct_2026_Network.yaml \
    --config-prefix=config \
    --template-paths=templates \
    --mechanisms-path=mechanisms/build \
    --dataset-prefix="$DATA_PREFIX" \
    --results-path=$results_path \
    --spike-input-path="${DATA_PREFIX}/Slice/CA1_Slice_100_dynamical_response_features_20250912.h5" \
    --spike-input-namespace='Spatiotemporal Feature Spikes drc_features_20250912' \
    --spike-input-attr='Spike Train' \
    --coordinates-namespace="Generated Coordinates" \
    --microcircuit-inputs \
    --io-size=10 \
    --tstop=9750 \
    --v-init=-77 \
    --dt=0.025 \
    --results-write-time=60 \
    --stimulus-onset=0.0 \
    --max-walltime-hours=3.9 \
    --verbose
