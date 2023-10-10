"""Test module."""
import unittest
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from pycode.io import load_raw_signal_from_hdf5
from pycode.operation import filter_signal
from pycode.spycode import Path_Generator
from pycode.utils import (Signals_Differences, is_monodimensional, make_column,
                          mea_60_electrode_index_to_label,
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


class TestArratUtils(unittest.TestCase):
    """Test the correctness of some array utility functions."""

    def test_monodimensional_array_checks(self):
        self.assertTrue(is_monodimensional(np.array([1, 2, 3])))
        self.assertTrue(is_monodimensional(np.array([[1, 2, 3]])))
        self.assertTrue(is_monodimensional(np.array([[1],
                                                     [2],
                                                     [3]])))
        self.assertFalse(is_monodimensional(np.array([[1, 1],
                                                      [2, 2],
                                                      [3, 3]])))

    def test_make_row(self):
        self.assertTrue((make_column(
            np.array([1, 2, 3])) == np.array([[1], [2], [3]])).all())
        self.assertTrue((
            make_column(np.array([[1], [2], [3]])) ==
            np.array([[1], [2], [3]])).all())
        self.assertTrue((make_column(
            np.array([[1, 2, 3]])) == np.array([[1], [2], [3]])).all())


def test_base_signal():
    BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
    H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
    ELECTRODE_NUMBER = 26  # random choise

    # acquire the signal of an electrode
    pg = Path_Generator(BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
    data_s = loadmat(pg.base_electrode_path(ELECTRODE_NUMBER))['data']
    data_h = load_raw_signal_from_hdf5(H5_FILE, ELECTRODE_NUMBER)

    sd = Signals_Differences(data_s, data_h)
    print(sd.max_err())
    print(sd.norm())
    sd.plot_signals()


def test_filtered_signal():
    BASE_FOLDER = Path('E:/PyCode/tests/34340/76/')
    H5_FILE = BASE_FOLDER.joinpath('34340_DIV43_100e_Stim_76.h5')
    ELECTRODE_NUMBER = 26  # random choise

    # acquire the signal of an electrode
    pg = Path_Generator(BASE_FOLDER, '34340_DIV43_100e_Stim_76.mcd')
    data_s = loadmat(pg.base_electrode_path(ELECTRODE_NUMBER))['data']
    filtered_data_s = loadmat(
        pg.filtered_electrode_path(ELECTRODE_NUMBER))['data']
    data_h = make_column(load_raw_signal_from_hdf5(H5_FILE, ELECTRODE_NUMBER))
    filtered_data_h = filter_signal(data_s, 10000, 70)

    plt.plot(filtered_data_s)
    sd = Signals_Differences(filtered_data_s, filtered_data_h)
    print(sd.max_err())
    print(sd.norm())
    sd.plot_signals()


def other_tests():
    # test_base_signal()
    test_filtered_signal()
    plt.show()


if __name__ == '__main__':

    other_tests()
    unittest.main()
