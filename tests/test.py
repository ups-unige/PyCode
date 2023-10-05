"""Test module."""
import unittest
from pathlib import Path

from scipy.io import loadmat

from pycode.io import load_raw_signal_from_hdf5
from pycode.spycode import Path_Generator
from pycode.utils import (mea_60_electrode_index_to_label,
                          mea_60_electrode_index_to_number,
                          mea_60_electrode_label_to_index,
                          mea_60_electrode_number_to_index)


class TestMeaIndexConversions(unittest.TestCase):
    """
    Tests the conversions between index and labels of MEA60 electrodes.
    """

    def test_number_to_index(self):
        self.assertEqual(mea_60_electrode_number_to_index(12), 1)
        self.assertEqual(mea_60_electrode_number_to_index(87), 60)
        self.assertEqual(mea_60_electrode_number_to_index(21), 7)
        self.assertEqual(mea_60_electrode_number_to_index(55), 35)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 11)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 18)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 20)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 29)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 70)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 79)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 81)
        self.assertRaises(Exception, mea_60_electrode_number_to_index, 88)
        self.assertEqual(mea_60_electrode_index_to_number(1), 12)
        self.assertEqual(mea_60_electrode_index_to_number(60), 87)
        self.assertEqual(mea_60_electrode_index_to_number(7), 21)
        self.assertEqual(mea_60_electrode_index_to_number(35), 55)
        self.assertRaises(Exception, mea_60_electrode_index_to_number, 0)
        self.assertRaises(Exception, mea_60_electrode_index_to_number, 61)

    def test_number_to_label(self):
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 11)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 18)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 20)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 29)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 70)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 79)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 81)
        self.assertRaises(Exception, mea_60_electrode_label_to_index, 88)
        self.assertRaises(Exception, mea_60_electrode_index_to_label, 0)
        self.assertRaises(Exception, mea_60_electrode_index_to_label, 61)


class TestSpycodeSimilarity(unittest.TestCase):
    """
    Tests the similarity between SpyCode processing and the custom made one.
    """
    BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
    H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
    SPYCODE_CONVERTED_FOLDER = BASE_FOLDER.joinpath(
        "34340_DIV43_100e_Stim_76/")

    def test_hdf5_converted_signals(self):
        """aaè
        Tests if a signal converted and loaded in HDF5 format is similar to
        the one converted with SpyCode.
        """

        # acquire the signal of an electrode
        electrode_number = 26
        pg = Path_Generator(self.BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
        matfile = loadmat(pg.base_electrode_path(electrode_number))
        print(matfile['data'].T)

        info_channel = load_raw_signal_from_hdf5(
            self.H5_FILE, electrode_number)[1]

        for i in range(0, 60):
            c = info_channel[i]
            print(c[0], c[1], c[4], mea_60_electrode_index_to_label(i))


if __name__ == '__main__':
    unittest.main()
