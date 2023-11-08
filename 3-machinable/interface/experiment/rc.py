from machinable import Component
import numpy as np
from pydantic import Field, BaseModel
from miv_simulator import simulator
from miv_simulator.lfp import LFP
from mpi4py import MPI
from typing import List
import sys
from miv_simulator import config
from miv_simulator.utils import from_yaml
from typing import Dict, Optional, Union
import logging

from machinable.config import to_dict
from machinable.utils import load_file


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
        stimulus: Optional[Union[str, List[float]]] = None
        t_end: float = 1000
        cells: str = Field("???")
        connections: str = Field("???")
        cell_types: config.CellTypes = Field("???")
        synapses: config.Synapses = Field("???")
        templates: str = "./simulation/templates"
        mechanisms: str = "./simulation/mechanisms"
        ranks: int = 8

    def on_write_meta_data(self):
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        return rank == 0

    def config_from_file(self, filename: str) -> Dict:
        return from_yaml(filename)

    def __call__(self):
        logging.basicConfig(level=logging.INFO)
        np.seterr(all="raise")

        h = simulator.configure_hoc(mechanisms_directory=self.config.mechanisms)
        env = simulator.ExecutionEnvironment(seed=self.seed)

        def log(m):
            if env.rank == 0:
                print(m)

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

        if self.config.stimulus:
            log("Creating stimulus")
            stimulus = self.config.stimulus
            if isinstance(stimulus, str):
                stimulus = load_file(self.config.stimulus)

            for gid, cell in env.artificial_cells["STIM"].items():
                if not (env.pc.gid_exists(gid)):
                    continue
                spike_train = np.array(stimulus)[int(gid) :: 10]
                print(f"{env.rank}: Stimulating with spike train {spike_train}")
                cell.play(h.Vector(spike_train))

        h.v_init = -65
        h.stdinit()
        h.secondorder = 2  # crank-nicholson
        h.dt = 0.025
        env.pc.timeout(600.0)

        h.finitialize(h.v_init)

        log("Finished initialization, starting the simulation")

        env.pc.psolve(self.config.t_end)

        log("Simulation finished, saving LFP")

        if env.rank == 0:
            out = np.column_stack([lfp.t, lfp.meanlfp])
            self.save_file("readout.npy", out)

    def readout(self):
        return self.load_file("readout.npy")
