"""Test module."""
from pathlib import Path

from h5py import File  # type: ignore

from pycode.spycode import Path_Generator

BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
SPYCODE_CONVERTED_FOLDER = BASE_FOLDER.joinpath("34340_DIV43_100e_Stim_76/")


def test_filtered_signal(electrode_number=25) -> bool:
    """
    Tests if a signal filtered with scipy is similar to the one filtered
    with SpyCode.
    """
    # acquire the signal of an electrode
    # TODO add in path generator a method to obtain the raw data of an
    # electrode of a phase
    pg = Path_Generator(BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
    print(pg.base_electrode_path(electrode_number).exists())
    print(pg.base_electrode_path(electrode_number))

    h5file = File(H5_FILE.absolute())
    print(h5file['Data']['Recording_0'].keys())
    return True


if __name__ == '__main__':
    test_filtered_signal()
