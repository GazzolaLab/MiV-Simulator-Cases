export DATA_PREFIX=./datasets

mpirun -n 8 run-network --verbose --arena-id A --stimulus-id Diag \
       --config-file=Microcircuit_Small.yaml \
       --template-paths templates \
        --dt 0.01 --tstop 2000 \
       --dataset-prefix $DATA_PREFIX \
       --config-prefix config \
       --results-path results/runs





