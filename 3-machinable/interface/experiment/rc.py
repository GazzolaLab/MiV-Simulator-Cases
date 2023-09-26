from machinable import Component
import numpy as np
from pydantic import Field, BaseModel
from miv_simulator.simulator import runtime, configure_hoc
from mpi4py import MPI
import sys
from miv_simulator import config
from miv_simulator.utils import from_yaml
from typing import Dict
import logging
from miv_simulator.lfp import LFP
from machinable.config import to_dict
from miv_simulator.coding import cast_spike_times


def mpi_excepthook(type, value, traceback):
    sys_excepthook(type, value, traceback)
    sys.stderr.flush()
    sys.stdout.flush()
    if MPI.COMM_WORLD.size > 1:
        MPI.COMM_WORLD.Abort(1)


sys_excepthook = sys.excepthook
sys.excepthook = mpi_excepthook


class Reservoir(Component):
    class Config(BaseModel):
        cells: str = Field("???")
        connections: str = Field("???")
        cell_types: config.CellTypes = Field("???")
        synapses: config.Synapses = Field("???")
        templates: str = "./simulation/templates"
        mechanisms: str = "./simulation/mechanisms"
        ranks_: int = 8
        nodes_: int = 1

    def config_from_file(self, filename: str) -> Dict:
        return from_yaml(filename)

    def __call__(self):
        logging.basicConfig(level=logging.INFO)
        np.seterr(all="raise")

        h = configure_hoc(mechanisms_directory=self.config.mechanisms)
        env = runtime.Env(seed=self.seed)

        env.load_cells(
            filepath=self.config.cells,
            cell_types=to_dict(self.config.cell_types),  # TODO: remove dict conversion
            templates=self.config.templates,
        )

        env.load_connections(
            filepath=self.config.connections,
            cell_filepath=self.config.cells,  # TODO: decouple
            synapses=self.config.synapses,
        )

        lfp = LFP(
            "ReadoutElectrode",
            env.pc,
            pop_gid_dict={
                pop_name: set(env.cells[pop_name].keys()).difference(
                    set(env.artificial_cells[pop_name].keys())
                )
                for pop_name in env.cells.keys()
            },
            pos=[500.0, 500.0, 0.0],  # top-center
            rho=333.0,
            dt_lfp=0.1,
            fdst=0.1,
            maxEDist=100.0,  # radius
            seed=self.seed + 1,
        )

        h.v_init = -65
        h.stdinit()
        h.secondorder = 2  # crank-nicholson
        h.dt = 0.025
        env.pc.timeout(600.0)

        h.finitialize(h.v_init)

        env.pc.psolve(0.0)
        for step in range(30):
            if env.rank == 0 and step % 10 == 0:
                print(f"Step {step} at t={h.t}")

            # random stimulation
            for gid, cell in env.artificial_cells["STIM"].items():
                if not (env.pc.gid_exists(gid)):
                    continue

                uniform_spike_train = cast_spike_times(
                    h.t + 1000 * np.random.uniform(size=10)
                )
                cell.play(h.Vector(uniform_spike_train))

            env.pc.psolve(h.t + 1.0)

        if env.rank == 0:
            print("Electrode activity: ", list(zip(lfp.t, lfp.meanlfp)))
