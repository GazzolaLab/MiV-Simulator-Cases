
mpirun.mpich -n 9 \
    optimize-network \
    --config-path=./config/optimize_network.yaml \
    --optimize-file-dir=results/network \
    --verbose \
    --nprocs-per-worker=8 \
    --n-iter=1 \
    --num-generations=200 \
    --no_cleanup \
    --dataset_prefix="datasets" \
    --config_prefix=./config \
    --results_path=$results_path \
    --results-path=results/network \
    --spike_input_path="datasets/Microcircuit_Small/Microcircuit_Small_input_spikes.h5" \
    --spike_input_namespace='Input Spikes' \
    --spike_input_attr='Spike Train' \
    --io_size=1 \
    --verbose
