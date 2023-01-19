#!/usr/bin/env python

from machinable import get

# Configure execution

get("mpi").as_default()


# Prepare and run simulation

network = get(
    "miv_simulator.interface.make_network",
    "~microcircuit",
).launch()

print("Obtaining synapse forests")

synapse_forest = {
    population: network.synapse_forest(
        {
            "population": population,
            "morphology": f"../1-construction/datasets/{population}.swc",
        }
    ).launch()
    for population in ["PYR", "PVBC", "OLM"]
}

print("Obtaining soma coordinates and measuring distances")

coordinates = network.soma_coordinates().launch()

measure_distances = coordinates.measure_distances().launch()

print("Obtaining distributed synapses along dendritic trees")

synapses = {
    population: coordinates.distribute_synapses(
        {
            "population": population,
            "forest": synapse_forest[population].output_filepath,
            "distribution": "poisson",
            "io_size": 1,
            "write_size": 0,
            "templates": "../1-construction/templates",
        }
    )
    for population in ["PYR", "PVBC", "OLM"]
}

print("Obtaining connections")

distance_connections = {
    population: coordinates.distance_connections(
        {
            "forest": synapse_forest[population].output_filepath,
            "connectivity_namespace": "Connections",
            "coordinates_namespace": "Generated Coordinates",
            "io_size": 1,
            "cache_size": 20,
            "write_size": 100,
        }
    )
    for population in ["PYR", "PVBC", "OLM"]
}

print("Obtaining input features")

input_features = coordinates.input_features({"populations": ("STIM",)}).launch()

print("Obtaining spike trains")

inputs = input_features.derive_spike_trains(
    {"populations": ("STIM",), "n_trials": 3}
).launch()

print("Prepare the data")

data = get(
    "miv_simulator.interface.prepare_data",
    uses=[
        network,
        coordinates,
        *synapse_forest.values(),
        *synapses.values(),
        *distance_connections.values(),
        inputs,
    ],
).launch()

print("Run the simulator")

simulation = get(
    "miv_simulator.interface.run",
    {
        "spike_input_path": inputs.output_filepath,
        "cells": data.output_filepath("cells"),
        "connections": data.output_filepath("connections"),
    },
)

simulation.launch()

print("Results are stored at ", simulation.local_directory())
