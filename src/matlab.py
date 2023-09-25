""" In this file there are the functions needed for communicate with MATLAB
Author: Mascelli Leonardo
Last Edited: 21-09-2023
"""

import os
import subprocess
from pathlib import Path
from typing import Union

import numpy as np


class iMatlabInterface:
    """
    This class is kind of an abstract class that generalize the method used to
    communicate with MATLAB.
    """
    library_path: Path

    def __init__(self, library_path: Union[str, Path],
                 cwd: Union[Path, str, None] = None,
                 wait: bool = False,
                 exit_: bool = True):
        """
        Set some params for MATLAB communication
        @param [in] library_path: the absolute path of the PyCode library
        @param [in] cwd: working directory for MATLAB runtime
        @param [in] wait: block program execution until the end of the MATLAB
                          process
        @param [in] exit_: close MATLAB instance at the end of the
                           communication
        """
        self.library_path = Path(library_path)
        self.cwd = cwd
        self.wait = wait
        self.exit = exit_

    def _script_folder(self) -> Path:
        """
        Returns the path of the MATLAB scripts in the PyCode library
        """
        return self.library_path.joinpath("pycode/matlab").absolute()

    def _add_prelude(self, code: str,
                     cwd: Union[Path, str, None] = None) -> str:
        """
        prepend the istructions to add the MATLAB scripts of PyCode to the
        path of the MATLAB libraries, setting the working directory
        """
        ml_prelude = f"""
    addpath '{self._script_folder()}/functions'
    addpath '{self._script_folder()}/classes'
    {'' if cwd is None else ('cd ' + str(cwd))}
    """
        return ml_prelude + code

    def run_code(self, _):
        raise Exception(args="Virtual method called")


class MatlabCLI(iMatlabInterface):
    """
    This class extend the iMatlabInterface so that it can use the command line
    to communicate with the MATLAB runtime
    """

    def __init__(self,
                 library_path: Union[str, Path],
                 cwd: Union[Path, str, None] = None,
                 wait: bool = True,
                 exit_: bool = True):
        """
        Set some params for MATLAB communication
        @param [in] library_path: the absolute path of the PyCode library
        @param [in] cwd: working directory for MATLAB runtime
        @param [in] wait: block program execution until the end of the MATLAB
                          process
        @param [in] exit_: close MATLAB instance at the end of the
                           communication
        """
        super().__init__(library_path, cwd, wait, exit_)

    def run_script(self, filepath: Path) -> None:
        """
        Execute a MATLAB script
        @param [in] filepath
        """
        if filepath.exists():
            cmd = (
                "matlab.exe -nodisplay -nosplash -nodesktop"
                f" -r \"run('{filepath}'); exit;"
            )
            os.system(cmd)
        else:
            print(f"ERROR: {filepath} not found")

    def run_code(
            self,
            code: str,
    ) -> Union[str, np.ndarray]:
        """
        Execute a fragment of MATLAB code
        @param [in] code
        """
        cmd = "matlab.exe -nosplash -nodesktop " \
              + f"{'-wait ' if self.wait else ''}" \
              + ' -r "' \
              + self._add_prelude(code, self.cwd) \
              + ';'
        if self.exit:
            cmd = cmd + 'exit;"'
        else:
            cmd = cmd + '"'
        cmd = cmd.replace('"', '\\"')
        cmd = cmd.replace("\n", "; ")
        print(cmd)
        return str(subprocess.check_output(cmd, shell=True))
