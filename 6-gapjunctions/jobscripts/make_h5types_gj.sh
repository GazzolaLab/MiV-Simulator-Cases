#!/bin/bash

make-h5types \
    --gap-junctions \
    -c Microcircuit_Small.yaml \
    --config-prefix config \
    --output-path datasets/MiV_h5types_gj.h5
