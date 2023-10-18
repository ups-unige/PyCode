"""PyCode input/output functions.

Author: Mascelli Leonardo
Last edited: 18-10-2023

This file contains a collection of functions for reading or writing the
experiment structures to file.
"""

from pathlib import Path
from typing import Dict, Optional

import numpy as np
from h5py import File
from scipy.io import loadmat

from .experiment import Experiment, Phase, PhaseInfo, Signal
from .utils import make_row


###############################################################################
#
#                       LOADING FROM MAT FILES
#
###############################################################################


def load_signal_from_mat(filepath: Path, sampling_frequency=10000)\
        -> Optional[Signal]:
    """
    load a signal from the given FILEPATH. If no SAMPLING_FREQUENCY is passed
    as second argument, the function create a Signal with the default value of
    10 KHz that is the default sampling frequency used by Multichannel Systems
    devices.
    It returns the Signal if the file was found and it is valid, None otherwise
    """
    try:
        # TODO check if data is the correct field of loaded mat
        return Signal(data=loadmat(filepath.absolute())['data'],
                      sampling_frequency=sampling_frequency,
                      path=filepath.absolute())
    except Exception as e:
        print(e.args)
        return None


def load_experiment_from_mat(filename: Path) -> Experiment:
    """
    A lot of confusion is confined into this function caused mainly by the
    complicated structures that scipy creates when converting a mat file.
    """
    try:
        data = loadmat(filename)
        ph_r, ph_c = data["phases"].shape
        try:
            date = data["date"][0]
        except Exception:
            date = ""
        if ph_r > ph_c:
            phases_mat = np.reshape(data["phases"][:], (ph_r, 1))
        else:
            phases_mat = np.reshape(data["phases"][0], (ph_c, 1))
        phases = []
        for phase_packed in phases_mat:
            phase = phase_packed[0]
            peaks_mat = phase["peaks"][0][0]
            peaks = {}
            for el in peaks_mat:
                try:
                    peaks[el[0][0][0]] = el[1][:, 0]
                except Exception:
                    peaks[el[0][0][0]] = np.array([])
            if phase["digital"][0][0].shape[0] > 1:
                digital = Signal(phase["digital"][0][0], 10e3)
            else:
                digital = None
            # here i set a default sampling frequency of 10 KHz and a duration
            # of the recording of 300 seconds.
            # TODO add those information to the relative MATLAB file as a
            # default
            try:
                sampling_frequency = phase["sampling_frequency"][0][0][0][0]
            except Exception:
                sampling_frequency = 10e3
            try:
                durate = phase["durate"][0][0][0][0]
            except Exception:
                durate = 300
            try:
                notes = phase["notes"][0][0][0][0]
            except Exception:
                notes = ""
            phases.append(
                Phase(
                    phase["name"][0][0][0],
                    peaks,
                    digital,
                    sampling_frequency,
                    durate,
                    notes,
                )
            )
    except Exception as e:
        assert False, e.args

    return Experiment(data["matrix_name"][0], data["path"][0], date, phases)


###############################################################################
#
#                           LOADING FROM HDF5 FILES
#
###############################################################################


def load_raw_signal_from_hdf5(filename: Path, electrode_index: int,
                              debug: bool = False) -> np.ndarray:
    h5file = File(filename.absolute(), 'r')
    # assume with digital
    # TODO test Steam_N position if recording has no digital signal
    # n_streams = h5file['/Data/Recording_0/AnalogStream/'].shape
    last_stream = len(h5file['/Data/Recording_0/AnalogStream'].keys()) - 1
    InfoChannel = h5file['/Data/Recording_0/AnalogStream/'
                         f'Stream_{last_stream}/InfoChannel']
    print(InfoChannel[electrode_index]) if debug else None
    ChannelData = h5file['/Data/Recording_0/AnalogStream/'
                         'Stream_{last_stream}/ChannelData']
    ADC_offset = InfoChannel[electrode_index][8]
    conversion_factor = InfoChannel[electrode_index][10]
    SCALING_FROM_VOLT_TO_MILLIVOLT = 6
    exponent = InfoChannel[electrode_index][7] + SCALING_FROM_VOLT_TO_MILLIVOLT

    mantissas = np.expand_dims(ChannelData[electrode_index][:], 1)

    converted_data = (mantissas-np.ones(shape=mantissas.shape)*ADC_offset) *\
        conversion_factor * np.power(10., exponent)
    return make_row(converted_data)


def load_peaks_from_hdf5(data) -> Dict[int, np.ndarray]:
    InfoTimeStamp = data['/InfoTimeStamp']

    indices = []
    map: Dict[int, int] = {}
    for i in range(InfoTimeStamp.shape[0]):
        print(i)
        # indices.append(index)
        # map[index] = label

    ret: Dict[int, np.ndarray] = {}

    for index in indices:
        label = map[index]
        ret[label] = None  # TODO fill with peaks

    return ret


def load_digital_from_hdf5(data, notes: Optional[str] = "") -> Signal:
    InfoChannel = data['InfoChannel']
    data_index = 0
    sampling_frequency: float = 1e6 / \
        InfoChannel[data_index][9]  # TODO check correct index

    ChannelData = data['ChannelData']
    signal_data = ChannelData[data_index]
    signal_data -= np.min(signal_data)

    return Signal(signal_data, sampling_frequency, notes)


def load_phase_from_hdf5(filename: Path,
                         info: Optional[PhaseInfo]) -> Phase:
    if info is not None:
        pass
    else:
        info = PhaseInfo.default_parse(filename)

    stream_index = 1 if info.digital else 0
    data = File(filename)['/Data/Recording_0']

    # checks if the data has a digital signal and the phase info too
    if info.digital and len(data['/AnalogStream']) == 1:
        raise Exception("info.digital is True but the phase does not contain"
                        " two Analog Streams")
    digital = load_digital_from_hdf5(
        data['AnalogStream/Stream_0/']) if info.digital else None

    return Phase(info.name,
                 peaks=load_peaks_from_hdf5(
                     data[f'/TimeStampStream/Stream_{stream_index}']),
                 digital=digital,
                 sampling_frequency=info.sampling_frequency,
                 durate=info.durate,
                 notes=info.notes,
                 )
