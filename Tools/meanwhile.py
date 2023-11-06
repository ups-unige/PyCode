"""
This script makes a TUI useful for getting informations during an experiment
for viewing and analizing result of a just registered cells activity
"""

from os import listdir
from pathlib import Path
from h5py import File
from pycode.io import load_phase_from_hdf5
from pycode.operation import rasterplot_phase

from matplotlib import pyplot as plt

# absolute path to the directory containing the phases hdf5
phases_path = Path("F:/03-11-2023/34341/hdf5")
phase_file = phases_path.joinpath("2023-11-03T17-08-5734341_DIV49_stim_3_65.h5")


phase = load_phase_from_hdf5(phase_file)
fig, ax = plt.subplots()
rasterplot_phase(phase, ax)
plt.show()
