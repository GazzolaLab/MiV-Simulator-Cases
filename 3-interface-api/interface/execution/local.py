import os
import shutil
import stat
import subprocess
import sys
from dataclasses import dataclass

from machinable import Execution


class LocalExecution(Execution):
    @dataclass
    class Config:
        mpi: str = "mpirun"

    def __call__(self):
        print("\n".join(self.pending_executables.map(lambda x: x.module)))
        print(
            f"\nSubmitting {len(self.pending_executables)} jobs ({len(self.executables)} total)."
        )
        for executable in self.pending_executables:
            if executable.config.get("ranks", 0) > 0:
                # run using MPI
                script_file = self.save_file(
                    f"mpi-{executable.id}.sh",
                    "#!/usr/bin/env bash\n\n" + executable.dispatch_code(),
                )
                st = os.stat(script_file)
                os.chmod(script_file, st.st_mode | stat.S_IEXEC)
                cmd = [
                    shutil.which(self.config.mpi),
                    "-n",
                    str(executable.config.get("ranks", 1)),
                    script_file,
                ]
                print(" ".join(cmd))
                with open(executable.local_directory("output.log"), "wb") as f:
                    p = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        env=os.environ,  # see https://stackoverflow.com/a/60070753
                    )
                    for o in iter(p.stdout.readline, b""):
                        sys.stdout.write(o.decode("utf-8"))
                        f.write(o)
            else:
                # default single-threaded execution
                executable.dispatch()
