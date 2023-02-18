export DATA_PREFIX=./datasets

mpirun -n 1 network-clamp go \
       -c Network_Clamp_PYR_gid_48041.yaml \
       --template-paths templates --dt 0.01 \
       -p PYR -g 48041  -t 250 \
       --dataset-prefix $DATA_PREFIX \
       --config-prefix config \
       --spike-events-path results/Microcircuit_4257574/Microcircuit_PYR_results.h5 \
       --spike-events-namespace 'Spike Events' \
       --results-path results/netclamp



