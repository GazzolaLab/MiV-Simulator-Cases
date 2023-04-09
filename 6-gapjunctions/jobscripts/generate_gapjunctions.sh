#!/bin/bash

mpirun.mpich -np 8 generate-gapjunctions \
             --config=./config/Microcircuit_Small.yaml \
             --types-path=./datasets/MiV_h5types_gj.h5 \
             --forest-path=./datasets/Microcircuit_Small/MiV_Cells_Microcircuit_Small_20220410.h5 \
             --connectivity-path=./datasets/Microcircuit_Small/MiV_gapjunctions_20230408.h5 \
             --connectivity-namespace="Gap Junctions" \
             --coords-path=./datasets/Microcircuit_Small/MiV_Cells_Microcircuit_Small_20220410.h5 \
             --coords-namespace="Generated Coordinates" \
             --io-size=4 -v 
