#!/usr/bin/env python

from machinable import get

# Configure execution

get("mpi").as_default()


# Prepare and run simulation

network = get(
    "miv_simulator.interface.make_network",
    "~microcircuit",
)
network.launch()

print("Obtaining soma coordinates and measuring distances")

coordinates = network.soma_coordinates()
coordinates.launch()

measure_distances = coordinates.measure_distances()
measure_distances.launch()

print("Obtaining distributed synapses along dendritic trees")
synapses = []
for population in ["PYR", "PVBC", "OLM"]:
    synapses.append(
        coordinates.distribute_synapses(
            {
                "population": population,
                "forest": network.synapse_forest(population),
                "distribution": "poisson",
                "io_size": 1,
                "write_size": 0,
                "templates": "../1-construction/templates",
            }
        )
    )
    synapses[-1].launch()

print("Obtaining connections")
distance_connections = []
for population in ["PYR", "PVBC", "OLM"]:
    distance_connections.append(
        coordinates.distance_connections(
            {
                "forest": network.synapse_forest(population),
                "connectivity_namespace": "Connections",
                "coordinates_namespace": "Generated Coordinates",
                "io_size": 1,
                "cache_size": 20,
                "write_size": 100,
            }
        )
    )
    distance_connections[-1].launch()

print("Obtaining input features")

input_features = coordinates.input_features({"populations": ("STIM",)})
input_features.launch()

print("Obtaining spike trains")

inputs = input_features.derive_spike_trains({"populations": ("STIM",), "n_trials": 3})
inputs.launch()

print("Prepare the data")

data = get(
    "miv_simulator.interface.prepare_data",
    uses=[network, coordinates, *synapses, *distance_connections, inputs],
)
data.launch()

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
