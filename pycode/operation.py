"""This file contains a collection of operations to apply to the experiments
Author: Mascelli Leonardo
Last Edited: 19-09-2023
"""

from typing import List, Optional, Tuple, Union

import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

from .experiment import Experiment, Phase
from .utils import intervals_boundaries, mea_60_electrode_list

###############################################################################
#                                                                             #
#                                   PLOTTING                                  #
#                                                                             #
###############################################################################


def rasterplot(phase: Phase,
               ax: Axes,
               with_digital: bool = False) -> Axes:
    """
    Draw the rasterplot of an experiment phase
    @param [in] phase
    @param [in] ax
    """
    electrodes = []
    spikes = []

    # peaks.keys() are the electrodes numbers
    for _, p in enumerate(phase.peaks.keys()):
        electrodes.append(p)
        spikes.append(phase.peaks[p][:])

    digital = phase.digital
    if digital is not None and with_digital:
        stim_intervals = intervals_boundaries(digital.data,
                                              digital.sampling_frequency)
        stim_rectangles = [
            Rectangle((x[0], 0), x[1] - x[0], 60) for x in stim_intervals
        ]
        patches = PatchCollection(
            stim_rectangles, facecolor="r", alpha=0.1, edgecolor="none"
        )
        # draw a collection of rettangles with 0.1 opacity to represent the
        # time where stimulus where active
        ax.add_collection(patches)
    ax.eventplot(spikes)  # , orientation='horizontal')
    return ax


###############################################################################
#                                                                             #
#                                STATISTICS                                   #
#                                                                             #
###############################################################################

def spikes_count(phase: Phase,
                 interval: Optional[Tuple[float, float]] = None
                 ) -> List[Tuple[int, int]]:
    """
    Compute the spike count of each electrode in a phase
    @param [in] phase
    @param [in] interval: an optional interval where to count the spikes
                          if None, the spikes will be counted on the whole
                          phase
    @returns a list with couple of (electrode number, spikes count)
    """

    ret = []
    if interval is not None:
        for electrode in phase.peaks.keys():
            peaks = np.where(np.all([phase.peaks[electrode] >= interval[0],
                                     phase.peaks[electrode] <= interval[1]],
                                    0))
            ret.append((electrode, len(peaks[0])))
    else:
        for electrode in phase.peaks.keys():
            ret.append((electrode, len(phase.peaks[electrode])))
    return ret


def mfr(experiment: Experiment,
        phase: Phase,
        interval: Optional[Tuple[float, float]] = None,
        net=False) -> Union[List[Tuple[int, float]], float]:
    """
    Compute the MFR (mean firing rate) of a given phase.
    @param [in] experiment
    @param [in] phase
    @param [in] interval: an optional interval where to compute the mfr
                          if None, the spikes will be counted on the whole
                          phase
    @param [in] net: if True it return the average of the channels
    @returns a list of the mfr of each channel or of the whole net
    """
    sc = spikes_count(phase, interval)
    if interval is not None:
        durate = interval[1] - interval[0]
    else:
        durate = phase.durate
    if net:
        ret = 0
        active_els = mea_60_electrode_list(experiment.grounded_el)
        for ael in active_els:
            for el, c in sc:
                if ael == el:
                    ret += c
        ret /= durate
    else:
        ret = []
        for el, c in sc:
            ret.append((el, c/durate))
    return ret


def psth(experiment: Experiment,
         phase: Phase,
         start: List[float],
         bin_size: float,
         bin_num: int,
         net=False) -> Union[List[Tuple[int, List[float]]], List[float]]:
    """
    Compute the PSTH (Post Stimulus Time Histogram) of a given phase.
    @param [in] experiment
    @param [in] phase
    @param [in] start: a list of initial time where to compute the psth
    @param [in] bin_size: the size of the interval
    @param [in] bin_num: on how many inteveral compute it
    @param [in] net: if True average the psth on all channels
    @returns a list of the psth of each channel or of the whole net
    """
    active_els = mea_60_electrode_list(experiment.grounded_el)
    ret_map = {}
    for el in active_els:
        ret_map[el] = []
        for _ in range(bin_num):
            ret_map[el].append(0)
    for bin_i in range(bin_num):
        for s in start[:-1]:  # TODO controllare che lo start dell'ultimo
            # intervallo sia precedente a (phase.durate - (bin_size*bin_num))
            sc = spikes_count(phase, (s, s+bin_size*bin_i))
            for ael in active_els:
                for el, c in sc:
                    if ael == el:
                        ret_map[el][bin_i] += c

    if not net:
        ret_not_net = []
        for el in ret_map.items():
            ret_not_net.append((el, ret_map[el]))
        return ret_not_net
    else:
        ret_net = []
        for _ in range(bin_num):
            ret_net.append(0)
        for el in ret_map.items():
            ret_net.append((el, ret_map[el]))
            for bin_i in range(bin_num):
                ret_net[bin_i] += ret_map[el][bin_i]
        return ret_net


def instantaneous_firing_rate(
        experiment: Experiment,
        phase: Phase,
        interval: Optional[Tuple[float, float]] = None) -> List[np.ndarray]:
    """
    Compute the instantaneous firing rate of a phase
    @param [in] phase
    @param [in] interval: an optional interval where to compute the mfr
                          if None, the spikes will be counted on the whole
                          phase
    @returns a list of the mfr of each channel or of the whole net
    """
    ret = []
    active_els = mea_60_electrode_list(experiment.grounded_el)
    for i in active_els:
        if i in phase.peaks.keys():
            if interval is not None:
                peaks = phase.peaks[i]
                interval_peaks = peaks[np.all([peaks >= interval[0],
                                               peaks <= interval[1]], 0)]
                ret.append(np.diff(interval_peaks))
            else:
                ret.append(np.diff(phase.peaks[i]))
        else:
            ret.append(np.array([]))
    return ret


###############################################################################
#                                                                             #
#                         SIGNAL PROCESSING                                   #
#                                                                             #
###############################################################################

# TODO respect the coding convenction of immutable objects

def set_intervals_to_zero(phase: Phase,
                          intervals: List[Tuple[float, float]]) -> Experiment:
    """
    Set to zero the selected intervals
    @param [in] phase
    @param [in] intervals: list of (start, end) of the intervals
    @returns a new experiment with the cleared intervals
    """
    els = phase.peaks.keys()
    for el in els:
        peaks = phase.peaks[el]
        for peak in peaks:
            for interval in intervals:
                if peak >= interval[0] and peak <= interval[1]:
                    peaks = peaks[peaks != peak]
                    break
        phase.peaks[el] = peaks


def clear_around_stimulation_boundaries(phase: Phase,
                                        guard: float) -> Experiment:
    """
    Clear at the beginning and at the end of the stimulation phase around and
    guard
    @param [in] phase
    @param [in] guard: duration (in seconds) of the guard
    @returns a new experiment with the cleared intervals
    """

    if phase.digital is not None:
        digital = phase.digital.data
        stimuli = intervals_boundaries(
            digital, phase.digital.sampling_frequency)
        intervals = []
        for x0, x1 in stimuli:
            intervals.append((x0, x0 + guard))
            intervals.append((x1, x1 + guard))
        set_intervals_to_zero(phase, intervals)

    else:
        assert False, "clearing around stimulation on a not stimulation phase"
