"""PyCode input/output functions.

Author: Mascelli Leonardo
Last edited: 19-09-2023

This file contains a collection of functions for reading or writing the
experiment structures to file.
"""

from pathlib import Path
from typing import Optional

import numpy as np
from h5py import File
from scipy.io import loadmat

from .experiment import Experiment, Phase, Signal

###############################################################################
# loading from mat files


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
# loading from hdf5 files


def load_raw_signal_from_hdf5(filename: Path, electrode_label: int):
    h5file = File(filename.absolute(), 'r')
    # assume with digital
    InfoChannel = h5file['/Data/Recording_0/AnalogStream/Stream_1/InfoChannel']
    ChannelData = h5file['/Data/Recording_0/AnalogStream/Stream_1/ChannelData']
    return (h5file, InfoChannel, ChannelData)
