"""PyCode utility functions
Author: Mascelli Leonardo
Last edited: 19-09-2023

This file contains some useful functions and constants for:
    * working with data in intervals
    * working with electrode index of MEAs
"""

from typing import List, Optional, Tuple, Union

import numpy as np

###############################################################################
#                                                                             #
#                                   SIGNALS                                   #
#                                                                             #
###############################################################################


class Signals_Differences:
    """
    This class is meant to be used to test if two signals are comparable and
    to provide some quantitative informations on where they are or are not
    """

    def __init__(self, signal1: np.ndarray, signal2: np.ndarray):
        """
        @constructor Compute the differences between two signals
        @param [in] signal1
        @param [in] signal2
        """
        pass


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
    ret = ret + list(range(82, 87))
    for g in grounded:
        ret = ret.remove(g)  # type: ignore
    return ret
