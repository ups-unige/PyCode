"""This file contains a collection of operations to apply to the experiments
Author: Mascelli Leonardo
Last Edited: 22-09-2023
"""

from copy import deepcopy
from typing import List, Optional, Tuple, Union

import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from scipy import signal

from .experiment import Experiment
from .utils import (intervals_boundaries, is_monodimensional,
                    mea_60_electrode_list)

###############################################################################
#                                                                             #
#                                   PLOTTING                                  #
#                                                                             #
###############################################################################


def rasterplot(experiment: Experiment,
               phase_index: int,
               ax: Axes,
               with_digital: bool = False) -> Axes:
    """
    Draw the rasterplot of an experiment phase
    @param [in] phase
    @param [in/out] ax
    @returns the same ax passed as argument
    """

    phase = experiment.phases[phase_index]
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

def spikes_count(experiment: Experiment,
                 phase_index: int,
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

    phase = experiment.phases[phase_index]
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
        phase_index: int,
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

    phase = experiment.phases[phase_index]
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
         phase_index: int,
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

    phase = experiment.phases[phase_index]
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
        phase_index: int,
        interval: Optional[Tuple[float, float]] = None) -> List[np.ndarray]:
    """
    Compute the instantaneous firing rate of a phase
    @param [in] phase
    @param [in] interval: an optional interval where to compute the mfr
                          if None, the spikes will be counted on the whole
                          phase
    @returns a list of the mfr of each channel or of the whole net
    """

    phase = experiment.phases[phase_index]
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

def filter_signal(data: np.ndarray, sampling_frequency: float,
                  cutoff: float, btype: str = 'highpass') -> np.ndarray:
    Wn = cutoff/(0.5*sampling_frequency)
    b, a = signal.butter(2, Wn, btype=btype)
    return signal.lfilter(b, a, data)


def compute_threshold(data: np.ndarray,
                      sf: float = 10000,
                      multCoeff: int = 8) -> float:
    assert is_monodimensional(
        data), "ERROR: compute_threshold. DATA should be monodimensional"
    nSamples = np.max(data.shape)  # number of points in data
    nWin = 30  # number of subdivision of the whole data
    winDur = 200e-3  # duration of the window where to compute the threshold
    winDur_samples = winDur*sf  # previous duration in samples
    sample_starting_points = np.arange(
        0, nSamples-1, np.round(nSamples/nWin), dtype=np.int32)
    sample_ending_points = np.round(
        sample_starting_points + np.int32(winDur_samples))
    threshold = 100

    for i_win in range(0, nWin):
        win_data = data[0, sample_starting_points[i_win]:
                        sample_ending_points[i_win]],
        new_threshold = np.std(win_data)
        if new_threshold > threshold:
            threshold = new_threshold

    return threshold*multCoeff


def spike_detection():
    """
NOTE:
    standard deviation coefficient: 8
    peak lifetime period PLP: 2.0 ms
    refractory period RP: 1.0 ms
    artecfact threshold (analog): 1 mV
    artefact threshold (electrode): 200 uV
    maximum stimulation frequency: 50 Hz
    sampling frequency: 10000 Hz

    algorithm:
        for each electrode:
        1. data = loadmat(electrode_file)['data']
        2. data = data - np.mean(data)
        2. auto compute threshold (data, sf=10000, multCoeff=8)
            1. nSamples = len(data)
            2. nWin = 30
            3. winDur = 200e-3;
            4. winDur_samples = winDur*sf;
            5. startSample = 1:(round(nSamples/nWin)):nSamples
            6. endSample = startSample+winDur_samples-1;
            7. th = 100;
            8. for i in range(0, nWin):
                thThis = np.std(data(startSample(i):endSample(i)))
                if th > thThis:
                    th = thThis
            9. th = th*multCoeff
    """


# TODO respect the coding convenction of immutable objects
# the way is probably through
# from copy import deepcopy
# and making deepcopy of experiment


def set_intervals_to_zero(
        experiment: Experiment,
        phase_index: int,
        intervals: List[Tuple[float, float]]) -> Experiment:
    """
    Set to zero the selected intervals
    @param [in] phase
    @param [in] intervals: list of (start, end) of the intervals
    @returns a new experiment with the cleared intervals
    """

    experiment_ = deepcopy(experiment)
    phase = experiment_.phases[phase_index]

    els = phase.peaks.keys()
    for el in els:
        peaks = phase.peaks[el]
        for peak in peaks:
            for interval in intervals:
                if peak >= interval[0] and peak <= interval[1]:
                    peaks = peaks[peaks != peak]
                    break
        phase.peaks[el] = peaks
    return experiment_


def clear_around_stimulation_boundaries(experiment: Experiment,
                                        phase_index: int,
                                        guard: float) -> Optional[Experiment]:
    """
    Clear at the beginning and at the end of the stimulation phase around and
    guard
    @param [in] phase
    @param [in] guard: duration (in seconds) of the guard
    @returns a new experiment with the cleared intervals
    """

    phase = experiment.phases[phase_index]

    if phase.digital is not None:
        digital = phase.digital.data
        stimuli = intervals_boundaries(
            digital, phase.digital.sampling_frequency)
        intervals = []
        for x0, x1 in stimuli:
            intervals.append((x0, x0 + guard))
            intervals.append((x1, x1 + guard))
        return set_intervals_to_zero(phase, intervals)
    else:
        assert False, "clearing around stimulation on a not stimulation phase"
