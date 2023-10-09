"""PyCode utility functions.

Author: Mascelli Leonardo
Last edited: 19-09-2023

This file contains some useful functions and constants for:
    * working with data in intervals
    * working with electrode index of MEAs
"""

from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

###############################################################################
#                                                                             #
#                                   SIGNALS                                   #
#                                                                             #
###############################################################################


def is_monodimensional(array: np.ndarray) -> bool:
    """
    Check if an array shape is 1 everywhere apart from at max one position.

    @param [in] array
    @returns the array is monodimensional or not
    """
    shape = array.shape
    dim_pos = np.where(shape == np.max(shape))[0]
    for i in range(len(shape)):
        if i != dim_pos and shape[i] != 1:
            return False
    return True


def make_column(array: np.ndarray) -> np.ndarray:
    assert is_monodimensional(
        array), "Error: make_raw, ARRAY should be monodimensional"
    size = np.max(array.shape)
    ret = np.reshape(array, (size, 1))
    return ret


class Signals_Differences:
    """
    This class is meant to be used to test if two signals are comparable and
    to provide some quantitative informations on where they are or are not
    """

    def __init__(self, signal1: np.ndarray, signal2: np.ndarray):
        """
        Compute the differences between two monodimensional signals.
        @param [in] signal1
        @param [in] signal2
        """

        assert is_monodimensional(signal1) and is_monodimensional(signal2), \
            "ERROR: input signals should be monodimensional"

        self.same_shape = signal1.shape == signal2.shape
        # store references of the signals as column arrays
        self.signal1 = make_column(signal1)
        self.signal2 = make_column(signal2)

    def max_err(self) -> Tuple[float, float, float]:
        mean_std = 0.5*np.std(self.signal1)+0.5*np.std(self.signal2)
        max_diff = np.max(self.signal1[0, :] - self.signal2[0, :])
        err_std = max_diff/mean_std
        max_err_std = np.max(err_std)
        max_err_s1 = max_diff/np.max(self.signal1)
        max_err_s2 = max_diff/np.max(self.signal2)
        return (max_err_std, max_err_s1, max_err_s2)

    def norm(self) -> float:
        diff_norm = np.sqrt(np.sum(np.power(self.signal1-self.signal2, 2)))
        signal1_norm = np.sqrt(np.sum(np.power(self.signal1, 2)))
        signal2_norm = np.sqrt(np.sum(np.power(self.signal2, 2)))
        assert signal1_norm != 0 and signal2_norm != 0, \
            "ERROR: Signals_Differences.norm signals should not be null"
        return (diff_norm/(signal1_norm+signal2_norm))

    def plot_signals(self):
        plt.plot(self.signal1)
        plt.plot(self.signal2)


###############################################################################
#                                                                             #
#                                   INTERVALS                                 #
#                                                                             #
###############################################################################


def data_in_intervals(
    data: np.ndarray, intervals: List[Tuple[int, int]]
) -> List[Tuple[np.ndarray, np.ndarray]]:
    """
    Returns a list of couple ([array of abscissa], [array of ordinate]) of the
    values in the intervals passed as parameters.
    @param [in] data: the data to be queried
    @param [in] intervals: a list of (initial time, final time) where to
                           extract the values
    @returns A list of tuple of arrays with the abscissa and the ordinate
             present in the queried intervals
    """
    ret = list()
    for i in intervals:
        start = i[0]
        end = i[1]
        ret.append(
            (np.linspace(start, end, end - start + 1),  # abscissa
             data[start: end + 1]))                     # ordinate
    return ret


def intervals_boundaries(
    data: np.ndarray, sampling_freq: Optional[float] = None
) -> List[Tuple[Union[int, float], Union[int, float]]]:
    """
    Returns a list of couple (init time, final time) of a signal where its
    value is 1 (or greater than 0).
    @param [in] data: the array to find positive intervals into
    @param [in] sampling_freq: if this value is provided the returned values
                               will be tranformed in time values instead of
                               indices
    @returns list of couple (initial time, final fime) of each interval
             where the signal is positive.
    """
    ret = list()
    # starting points of an interval are those where the first derivative is
    # positive
    intervals_indices_start = np.where(np.gradient(data[:, 0]) > 0)[0]
    # ending points of an interval are those where the first derivative is
    # negative
    intervals_indices_ends = np.where(np.gradient(data[:, 0]) < 0)[0]

    for i, n in enumerate(intervals_indices_start):
        if sampling_freq is not None:
            ret.append(
                # dividing by the sampling frequency gives the time value
                (n / sampling_freq, intervals_indices_ends[i] / sampling_freq))
        else:
            ret.append((n, intervals_indices_ends[i]))
    return ret


def average_waves(
    signal: np.ndarray,
    digital: np.ndarray,
    guard: Tuple[float, float] = (0, 0),
    max_intervals=0
) -> np.ndarray:
    """
    Average all the interval of SIGNAL where DIGITAL is positive escluding a
    GUARD (measured in fraction)
    @param [in] signal: the signal to be spitted
    @param [in] digital: the signal used to decide the splitting intervals
    @param [in] guard: a couple of value representing the fraction of the
                       interval to use as a guard after start and end
    @param [in] max_waves: no more than so many intervals
    @returns a single array with the average of all the intervals
    """
    intervals = intervals_boundaries(digital)
    if max_intervals > 0:
        intervals = intervals[:max_intervals]

    intervals_with_guard = []
    for i in intervals:
        i_len = i[1] - i[0]  # total duration of the interval
        intervals_with_guard.append(
            # add to the start and the end a fraction of the total duration of
            # the interval
            (i[0] + guard[0] * i_len, i[1] + guard[1] * i_len))

    waves = data_in_intervals(signal, intervals_with_guard)

    ret = np.zeros(shape=waves[0][1].shape)  # accumulator variable

    for w in waves:
        shaper, shapew = ret.shape, w[1].shape
        if shapew[0] > shaper[0]:
            tmp = ret + w[1][: shaper[0]]
        else:
            tmp = ret[: shapew[0]] + w[1]
        ret = tmp

    return ret / len(waves)


###############################################################################
#                                                                             #
#                                  ELECTRODES                                 #
#                                                                             #
###############################################################################


MEA_60_MIN = 12
MEA_60_MAX = 86


def mea_60_electrode_list(grounded: List[int] = []) -> List[int]:
    """
    Generates a list of values representing the electrodes index of a MEA60.
    @param [in] grounded: a list of value to esclude from the return
    @returns a list of index
    """
    ret: List[int] = []
    ret = ret + list(range(12, 18))
    for i in range(2, 8):
        ret = ret + list(range(i * 10 + 1, i * 10 + 9))
    ret = ret + list(range(82, 88))
    for g in grounded:
        ret = ret.remove(g)  # type: ignore
    return ret


full_mea_60 = mea_60_electrode_list()
MEA_INDEX_LABEL = {
    0: 47,
    1: 48,
    2: 46,
    3: 45,
    4: 38,
    5: 37,
    6: 28,
    7: 36,
    8: 27,
    9: 17,
    10: 26,
    11: 16,
    12: 35,
    13: 25,
    14: 15,
    15: 14,
    16: 24,
    17: 34,
    18: 13,
    19: 23,
    20: 12,
    21: 22,
    22: 33,
    23: 21,
    24: 32,
    25: 31,
    26: 44,
    27: 43,
    28: 41,
    29: 42,
    30: 52,
    31: 51,
    32: 53,
    33: 54,
    34: 61,
    35: 62,
    36: 71,
    37: 63,
    38: 72,
    39: 82,
    40: 73,
    41: 83,
    42: 64,
    43: 74,
    44: 84,
    45: 85,
    46: 75,
    47: 65,
    48: 86,
    49: 76,
    50: 87,
    51: 77,
    52: 66,
    53: 78,
    54: 67,
    55: 68,
    56: 55,
    57: 56,
    58: 58,
    59: 57,
}


def mea_60_electrode_index_to_label(index: int) -> int:
    """
    Return the corresponding electrode label (in the range 12-87) from an
    index (in the range 0-59). Their labelling pattern is:

               20 18 15 14 11  9               12 13 14 15 16 17
            23 21 19 16 13 10  8  6         21 22 23 24 25 26 27 28
            25 24 22 17 12  7  5  4         31 32 33 34 35 36 37 38
            28 29 27 26  3  2  0  1  <----> 41 42 43 44 45 46 47 48
            31 30 32 33 56 57 59 58         51 52 53 54 55 56 57 58
            34 35 37 42 47 52 54 55         61 62 63 64 65 66 67 68
            36 38 40 43 46 49 51 53         71 72 73 74 75 76 77 78
               39 41 44 45 48 50               82 83 84 85 86 87
    """
    if not (index >= 0 and index < 60):
        raise Exception("Error: INDEX should be in range [1-60]")
    return MEA_INDEX_LABEL[index]


MEA_LABEL_INDEX = {
    47: 0,
    48: 1,
    46: 2,
    45: 3,
    38: 4,
    37: 5,
    28: 6,
    36: 7,
    27: 8,
    17: 9,
    26: 10,
    16: 11,
    35: 12,
    25: 13,
    15: 14,
    14: 15,
    24: 16,
    34: 17,
    13: 18,
    23: 19,
    12: 20,
    22: 21,
    33: 22,
    21: 23,
    32: 24,
    31: 25,
    44: 26,
    43: 27,
    41: 28,
    42: 29,
    52: 30,
    51: 31,
    53: 32,
    54: 33,
    61: 34,
    62: 35,
    71: 36,
    63: 37,
    72: 38,
    82: 39,
    73: 40,
    83: 41,
    64: 42,
    74: 43,
    84: 44,
    85: 45,
    75: 46,
    65: 47,
    86: 48,
    76: 49,
    87: 50,
    77: 51,
    66: 52,
    78: 53,
    67: 54,
    68: 55,
    55: 56,
    56: 57,
    58: 58,
    57: 59,
}


def mea_60_electrode_label_to_index(label: int) -> int:
    """
    Return the corresponding index (in the range 0-59) from an electrode
    label (in the range 12-87).

              12 13 14 15 16 17                20 18 15 14 11  9
           21 22 23 24 25 26 27 28          23 21 19 16 13 10  8  6
           31 32 33 34 35 36 37 38          25 24 22 17 12  7  5  4
           41 42 43 44 45 46 47 48  <---->  28 29 27 26  3  2  0  1
           51 52 53 54 55 56 57 58          31 30 32 33 56 57 59 58
           61 62 63 64 65 66 67 68          34 35 37 42 47 52 54 55
           71 72 73 74 75 76 77 78          36 38 40 43 46 49 51 53
              82 83 84 85 86 87                39 41 44 45 48 50
    """
    if label not in full_mea_60:
        raise Exception("Error: LABELL should be a valide electrode number")
    return MEA_LABEL_INDEX[label]
