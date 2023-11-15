from pathlib import Path
from pycode.hdf5 import H5Content
import matplotlib.pyplot as plt  # type: ignore

TEST_FILE = Path(
    "E:/unige/raw data/03-10-2023/34341/hdf5/34341_DIV49_ele_10_3V_el55.h5"
)
if __name__ == "__main__":
    content = H5Content(TEST_FILE)
    plt.plot(content.analogs[0].parse_signal(0))
    plt.show()
