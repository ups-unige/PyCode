"""Test module."""
import unittest
from pathlib import Path

import numpy as np
from scipy.io import loadmat

from pycode.io import load_raw_signal_from_hdf5
from pycode.spycode import Path_Generator
from pycode.utils import (mea_60_electrode_index_to_label,
                          mea_60_electrode_label_to_index)


class TestMeaIndexConversions(unittest.TestCase):
    """Tests the conversions between index and labels of MEA60 electrodes."""

    def test_number_to_label(self):
        """Test conversions betweens circular labeling and indexing."""
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 11)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 18)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 20)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 29)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 70)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 79)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 81)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 88)
        self.assertRaises(Exception, mea_60_electrode_index_to_label, -1)
        self.assertRaises(Exception, mea_60_electrode_index_to_label, 60)


class TestSpycodeSimilarity(unittest.TestCase):
    """Tests the similarity between SpyCode processing and the custom made."""

    BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
    H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
    SPYCODE_CONVERTED_FOLDER = BASE_FOLDER.joinpath(
        "34340_DIV43_100e_Stim_76/")
    ELECTRODE_NUMBER = 26  # random choise

    def test_hdf5_converted_signals(self):
        """Tests similatiry between signal converted with SpyCode and HDF5."""
        # acquire the signal of an electrode
        pg = Path_Generator(self.BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
        matfile = loadmat(pg.base_electrode_path(self.ELECTRODE_NUMBER))

        print(matfile['data'].T)
        print(load_raw_signal_from_hdf5(self.H5_FILE, self.ELECTRODE_NUMBER))


if __name__ == '__main__':
    unittest.main()
