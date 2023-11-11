"""
Here i want to test the load_phase_from_hdf5 with a test file
"""

from pathlib import Path
from pycode.hdf5 import H5Content
import matplotlib.pyplot as plt
from h5py import File

TEST_FILE = Path(
    "E:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_stim_4_60.h5"
)  # noqa
if __name__ == "__main__":
    content = H5Content(TEST_FILE)
    # for i, analog in enumerate(content.analogs):
    #     print(i)
    #     print(analog)

    # plt.plot(content.analogs[2].parse_signal(0))
    # plt.show()
