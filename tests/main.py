"""
Here i want to test the load_phase_from_hdf5 with a test file
"""
from pathlib import Path
from pycode.io import load_phase_from_hdf5
from h5py import File

TEST_FILE = Path("E:/unige/PyCode/tests/data/experimenter_test/00000_DIV40_Stim_1_60.h5")  # noqa
phase = load_phase_from_hdf5(TEST_FILE)
for key in phase.peaks.keys():
    print(phase.peaks[key])
# with File(TEST_FILE) as data:
#    print(data['/Data/Recording_0/TimeStampStream/Stream_0/TimeStampEntity_0'][0])
