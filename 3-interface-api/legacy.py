#!/usr/bin/env python
from machinable import get, Element

with get("interface.execution.local"):
    h5_types = get(
        "miv_simulator.interface.h5_types",
        {
            "cell_distributions": {  # "from_file('simulation/config/cell_distributions.yml')",  # {
                "STIM": {"SO": 0, "SP": 10, "SR": 0, "SLM": 0},
                "PYR": {"SO": 0, "SP": 80, "SR": 0, "SLM": 0},
                "PVBC": {"SO": 35, "SP": 10, "SR": 8, "SLM": 0},
                "OLM": {"SO": 44, "SP": 0, "SR": 0, "SLM": 0},
            },
            "synapses": "from_file('simulation/config/synapses.yml')",
        },
    ).launch()
    print(h5_types.local_directory())

    print("Obtain network architecture")

    network = get(
        "miv_simulator.interface.network_architecture",
        {
            "filepath": h5_types.output_filepath,
            "cell_distributions": h5_types.config.cell_distributions,
            "synapses": h5_types.config.synapses,
            "layer_extents": {  # }"from_file('simulation/config/layer_extents.yml')",  # {
                "SO": [[0.0, 0.0, 0.0], [1000.0, 1000.0, 100.0]],
                "SP": [[0.0, 0.0, 100.0], [1000.0, 1000.0, 150.0]],
                "SR": [[0.0, 0.0, 150.0], [1000.0, 1000.0, 350.0]],
                "SLM": [[0.0, 0.0, 350.0], [1000.0, 1000.0, 450.0]],
            },
            "cell_constraints": {
                "PC": {"SP": [100, 120]},
                "PVBC": {"SR": [150, 200]},
            },
        },
    ).launch()

    print("Obtaining soma coordinates and measuring distances")

    measure_distances = network.measure_distances().launch()

    print("Obtaining synapse forests")

    synapse_forest = {
        population: network.generate_synapse_forest(
            {
                "population": population,
                "morphology": f"./simulation/morphology/{population}.swc",
            }
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    print("Obtaining distributed synapses along dendritic trees")
    synapses = {
        population: network.distribute_synapses(
            {
                "forest_filepath": synapse_forest[population].output_filepath,
                "cell_types": "from_file('simulation/config/cell_types.yml')",
                "population": population,
                "distribution": "poisson",
                "mechanisms_path": "./simulation/mechanisms",
                "template_path": "./simulation/templates",
                "io_size": 1,
                "write_size": 0,
            }
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    print("Obtaining connections")

    connections = {
        population: network.generate_connections(
            {
                "forest_filepath": synapses[population].output_filepath,
                "axon_extents": "from_file('simulation/config/axon_extents.yml')",
                "template_path": "./simulation/templates",
                "io_size": 1,
                "cache_size": 20,
                "write_size": 100,
            }
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    input_features = get(
        "miv_simulator.interface.legacy.input_features",
        [
            {
                "config_filepath": "simulation/config/legacy/default.yaml",
                "coordinates": network.config.filepath,
                "populations": ("STIM",),
            }
        ],
        uses=network,
    ).launch()

    print("Obtaining spike trains")

    inputs = input_features.derive_spike_trains(
        {"populations": ("STIM",), "n_trials": 3}
    ).launch()

    # print("Adding custom spike data")
    # inputs.from_numpy({gid: np.random.randint(20) for gid in range(1000)})

    print("Prepare the data")

    data = get(
        "miv_simulator.interface.legacy.prepare_data",
        uses=[
            network,
            *synapse_forest.values(),
            *synapses.values(),
            *connections.values(),
            inputs,
        ],
    ).launch()

    print("Run the simulator")

    simulation = Element.make(
        "miv_simulator.interface.legacy.run",
        {
            "config_filepath": "simulation/config/legacy/default.yaml",
            "spike_input_path": inputs.output_filepath,
            "cells": data.output_filepath("cells"),
            "connections": data.output_filepath("connections"),
            "templates": "./simulation/templates",
            "mechanisms": "./simulation/mechanisms",
            "spike_input_namespace": inputs.active_spike_input_namespace,
            "spike_input_attr": inputs.active_spike_input_attr,
            "ranks_": 1,
        },
        uses=[inputs, data],
    )

    simulation.launch()

    print("Results located at ", simulation.local_directory())

    print(
        {
            "cells": data.output_filepath("cells"),
            "connections": data.output_filepath("connections"),
        }
    )
