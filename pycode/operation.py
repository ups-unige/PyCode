"""This file contains a collection of operations to apply to the experiments
Author: Mascelli Leonardo
Last Edited: 22-09-2023
"""

from copy import deepcopy
from typing import List, Optional, Tuple, Union

import numpy as np  # type: ignore
from matplotlib.axes import Axes  # type: ignore
from matplotlib.collections import PatchCollection  # type: ignore
from matplotlib.patches import Rectangle  # type: ignore
from scipy import signal  # type: ignore

from .experiment import Experiment, Phase
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


def rasterplot_phase(phase: Phase,
                     ax: Axes,
                     with_digital: bool = False) -> Axes:
    """
    Draw the rasterplot of an experiment phase
    @param [in] phase
    @param [in/out] ax
    @returns the same ax passed as argument
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


def plot_signal_with_spikes(signal: np.ndarray,
                            events: np.ndarray,
                            ax: Axes,) -> Axes:
    """Draw the given signal and a symbol where the events are releaved.
    The user must ensure that the abscissa of the signal and the events
    are coherent.
    @param [in] signal
    @param [in] events
    @param [in] ax: the Axes where to draw the plot
    @returns the same ax passed as argument
    """
    ax.plot(signal)
    ax.plot(events, '*')
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
    """
    Automatically find a threshold for spike detection
    @param [in] data: signal to process
    @param [in] sf: sampling frequency
    @param [in] multCoeff: how many std use as threshold
    @returns the computed threshold

    This algorithm as well as the spike_detection_core one have been
    taken from the SpyCode tool so the merit of it is to be attribuite
    to its authors.
    The algorithm splits the signal in NWIN parts and in each of those
    computes the std in a period of 300ms and takes the smaller.
    """

    assert is_monodimensional(
        data), "ERROR: compute_threshold. DATA should be monodimensional"
    nSamples = np.max(data.shape)  # number of points in data
    nWin = 30  # number of subdivision of the whole data
    winDur = 200e-3  # duration of the window where to compute the threshold
    winDur_samples = winDur*sf  # previous duration in samples
    sample_starting_points = np.arange(
        0, nSamples-1, np.round(nSamples/nWin), dtype=np.int32)
    sample_ending_points = np.round(
        sample_starting_points + int(winDur_samples))
    threshold = 100

    for i_win in range(0, nWin):
        win_data = data[0, sample_starting_points[i_win]:
                        sample_ending_points[i_win]],
        new_threshold = np.std(win_data)
        if new_threshold < threshold:
            threshold = new_threshold

    return threshold*multCoeff


def spike_detection_core(data: np.ndarray,
                         threshold: float,
                         peakDuration: float,
                         refrTime: float,
                         sampling_frequency: float
                         ) -> Tuple[np.ndarray, np.ndarray]:
    """
    The core routine of the spikes detection.

    @param [in] data: array where to look for peaks
    @param [in] threshold
    @param [in] peakDuration: in milliseconds
    @param [in] refrTime: in milliseconds
    @param [in] sampling_frequency: in Hz
    @returns a tuple of arrays with peaks value and peaks time
    """

    assert is_monodimensional(
        data), "ERROR: spike_detection_core. DATA should be monodimensional"

    OVERLAP = 5
    nSamples = np.max(data.shape)  # number of points in data
    ret = (np.zeros(nSamples), np.zeros(nSamples))

    # Convertion from milliseconds to number of samples
    SCALING_MS_TO_S = 1/1000
    peakDuration = np.round(peakDuration*SCALING_MS_TO_S*sampling_frequency)
    refrTime = np.round(refrTime*SCALING_MS_TO_S*sampling_frequency)

    newIndex = 1
    indexPeak = 1
    interval = 0.
    sTimePeak = 0
    eTimePeak = 0
    sValuePeak = 0.
    eValuePeak = 0.

    for index in range(2, nSamples-1):
        if index < newIndex:
            continue

        if (np.abs(data[0, index]) > np.abs(data[0, index-1])) and \
                (np.abs(data[0, index]) >= np.abs(data[0, index+1])):
            sTimePeak = index
            sValuePeak = data[0, index]

            if (index+peakDuration) > nSamples:
                interval = nSamples - index
            else:
                interval = peakDuration

            if sValuePeak > 0:
                eTimePeak = index + 1
                eValuePeak = sValuePeak

                for i in range(index+1, int(index+interval)):
                    if data[0, i] < eValuePeak:
                        eTimePeak = i
                        eValuePeak = data[0, i]
                for i in range(index+1, int(eTimePeak)):
                    if data[0, i] > sValuePeak:
                        sTimePeak = i
                        sValuePeak = data[0, i]

                if eTimePeak == (index+interval) and \
                        (index+interval+OVERLAP) < nSamples:
                    for i in range(eTimePeak+1, int(index+interval+OVERLAP+1)):
                        if data[0, i] < eValuePeak:
                            eTimePeak = i
                            eValuePeak = data[0, i]
            else:
                eTimePeak = index + 1
                eValuePeak = sValuePeak

                for i in range(index+1, int(index+interval)):
                    if data[0, i] > eValuePeak:
                        eTimePeak = i
                        eValuePeak = data[0, i]
                for i in range(index+1, eTimePeak):
                    if data[0, i] < sValuePeak:
                        sTimePeak = i
                        sValuePeak = data[0, i]

                if eTimePeak == (index+interval) and \
                        (index+interval+OVERLAP) < nSamples:
                    for i in range(eTimePeak+1, int(index+interval+OVERLAP+1)):
                        if data[0, i] > eValuePeak:
                            eTimePeak = i
                            eValuePeak = data[0, i]

            if np.abs(sValuePeak - eValuePeak) >= threshold:
                ret[0][indexPeak] = np.abs(sValuePeak-eValuePeak)

                if np.abs(sValuePeak) > np.abs(eValuePeak):
                    ret[1][indexPeak] = sTimePeak
                else:
                    ret[1][indexPeak] = eTimePeak

                if (ret[1][indexPeak]+refrTime) > eTimePeak and \
                        (ret[1][indexPeak] + refrTime) < nSamples:
                    newIndex = ret[1][indexPeak] + refrTime
                else:
                    newIndex = eTimePeak + 1

                indexPeak = indexPeak + 1

    return ret


def spike_detection(data: np.ndarray) -> Tuple[np.ndarray,
                                               np.ndarray]:
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
        3. auto compute threshold (data, sf=10000, multCoeff=8)
    """
    data_mean = np.mean(data, axis=1)
    data = data-data_mean
    return spike_detection_core(data,
                                compute_threshold(data),
                                2,
                                1,
                                10000)


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
