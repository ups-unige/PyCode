"""Test module."""
import unittest
from pathlib import Path

from h5py import File  # type: ignore

from pycode.spycode import Path_Generator
from pycode.utils import (mea_60_electrode_index_to_number,
                          mea_60_electrode_number_to_index)

BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
SPYCODE_CONVERTED_FOLDER = BASE_FOLDER.joinpath("34340_DIV43_100e_Stim_76/")


class TestMeaIndexConversions(unittest.TestCase):
    """
    Tests the conversions between index and labels of MEA60 electrodes.
    """

    def test_number_to_index(self):
        self.assertEqual(mea_60_electrode_number_to_index(12), 1)
        self.assertEqual(mea_60_electrode_number_to_index(21), 7)


def test_filtered_signal(electrode_number=25) -> bool:
    """
    Tests if a signal filtered with scipy is similar to the one filtered
    with SpyCode.
    """

    # acquire the signal of an electrode
    # pg = Path_Generator(BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
    # print(pg.base_electrode_path(electrode_number).exists())
    # print(pg.base_electrode_path(electrode_number))

    h5file = File(H5_FILE.absolute())
    h5file.visit(lambda x: print(x, type(h5file[x]), sep='\t\t\t\t\t'))
    # print(h5file['Data']['Recording_0']['AnalogStream']['Stream_0']['InfoChannel'])#.keys())

    # print(h5file['Data/Recording_0/AnalogStream/Stream_1/ChannelData'])
    print(mea_60_electrode_number_to_index(12))
    return True


if __name__ == '__main__':
    unittest.main()
