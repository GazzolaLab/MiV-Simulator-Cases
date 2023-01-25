import subprocess

from machinable import Execution


class MPI(Execution):
    def on_dispatch(self):
        for experiment in self.experiments:
            if experiment.config.get("ranks_", 0) > 0:
                # run using MPI
                print(
                    subprocess.check_output(
                        [
                            "mpirun",
                            "-n",
                            str(experiment.config.ranks_),
                            self.save_file(
                                f"mpi-{experiment.experiment_id}.sh",
                                experiment.dispatch_code(),
                            ),
                        ]
                    ).decode("ascii")
                )
            else:
                # default single-threaded execution
                experiment()
