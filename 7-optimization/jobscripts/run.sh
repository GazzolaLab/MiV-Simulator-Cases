#!/bin/bash

mpirun -np 12 run-network \
       --config-file=Microcircuit_Small.yaml  \
       --config-prefix=config \
       --arena-id=A \
       --stimulus-id=Diag \
       --template-paths=templates \
       --dataset-prefix="./datasets" \
       --results-path=results \
       --io-size=1 \
       --tstop=500 \
       --v-init=-75 \
       --results-write-time=60 \
       --stimulus-onset=0.0 \
       --max-walltime-hours=0.49 \
       --dt 0.025 \
       --verbose
