from machinable import get
from miv_simulator.config import Config


SOURCE = "./simulation"
CONFIG = "config/microcircuit.yml"

config = Config.from_yaml(f"{SOURCE}/{CONFIG}")

with get("interface.execution.local"):

    h5_types = get(
        "miv_simulator.interface.h5_types",
        [
            {
                "cell_distributions": config.cell_distributions,
                "projections": config.projections,
            },
            # reduce number of neurons for this example
            {"cell_distributions": {
                "STIM": {"SO": 0, "SP": 10, "SR": 0, "SLM": 0},
                "PYR": {"SO": 0, "SP": 80, "SR": 0, "SLM": 0},
                "PVBC": {"SO": 35, "SP": 10, "SR": 8, "SLM": 0},
                "OLM": {"SO": 44, "SP": 0, "SR": 0, "SLM": 0},
            }}
        ],
    ).launch()

    network = get(
        "miv_simulator.interface.network_architecture",
        {
            "filepath": h5_types.output_filepath,
            "cell_distributions": h5_types.config.cell_distributions,
            "layer_extents": config.layer_extents,
        },
        uses=h5_types,
    ).launch()

    measure_distances = network.measure_distances().launch()

    synapse_forest = {
        population: network.generate_synapse_forest(
            {
                "population": population,
                "morphology": f"{SOURCE}/morphology/{population}.swc",
            },
            uses=measure_distances,
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    synapses = {
        population: network.distribute_synapses(
            {
                "forest_filepath": synapse_forest[population].output_filepath,
                "cell_types": config.cell_types,
                "population": population,
                "distribution": "poisson",
                "mechanisms_path": f"{SOURCE}/mechanisms",
                "template_path": f"{SOURCE}/templates",
                "io_size": 1,
                "write_size": 0,
            },
            uses=list(synapse_forest.values()),
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    connections = {
        population: network.generate_connections(
            {
                "synapses": config.synapses,
                "forest_filepath": synapses[population].output_filepath,
                "axon_extents": config.axon_extents,
                "template_path": f"{SOURCE}/templates",
                "io_size": 1,
                "cache_size": 20,
                "write_size": 100,
            },
            uses=list(synapses.values()),
        ).launch()
        for population in ["PYR", "PVBC", "OLM"]
    }

    graph = get(
        "miv_simulator.interface.neuroh5_graph",
        uses=[
            network,
            *synapse_forest.values(),
            *synapses.values(),
            *connections.values(),
        ],
    ).launch()

print('Constructed microcircuit model:')
print(graph.files())

