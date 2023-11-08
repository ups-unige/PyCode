"""PyCode input/output functions.

Author: Mascelli Leonardo
Last edited: 31-10-2023

This file contains a collection of functions for reading or writing the
experiment structures to file.
"""

from pathlib import Path
from typing import Dict, List, Optional

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
    """
    Load and convert a raw signal acquired with Multichannel Systems
    instrumentation.
    @param [in] filename: the path of the raw file
    @param [in] electrode_index: the index of the electrode
    TODO convert it into the label of the electrode
    @param [in] debug: debug flag (prints the InfoChannel fields if True)
    @returns an array with the recorded voltages values
    """

    h5file = File(filename.absolute(), 'r')

    # get the last stream if the AnalogStream level, the previous ones may be
    # some recorded trigger events
    last_stream = len(h5file['/Data/Recording_0/AnalogStream'].keys()) - 1

    InfoChannel = h5file[('/Data/Recording_0/AnalogStream/'
                         f'Stream_{last_stream}/InfoChannel')]
    print(InfoChannel[electrode_index]) if debug else None

    ChannelData = h5file[('/Data/Recording_0/AnalogStream/'
                         f'Stream_{last_stream}/ChannelData')]

    # here all the parameter for converting the ADC values to the actual
    # voltage are got from the InfoChannel struct
    ADC_offset = InfoChannel[electrode_index][8]
    conversion_factor = InfoChannel[electrode_index][10]
    SCALING_FROM_VOLT_TO_MILLIVOLT = 6
    exponent = InfoChannel[electrode_index][7] + SCALING_FROM_VOLT_TO_MILLIVOLT
    mantissas = np.expand_dims(ChannelData[electrode_index][:], 1)

    converted_data = (mantissas-np.ones(shape=mantissas.shape)*ADC_offset) *\
        conversion_factor * np.power(10., exponent)

    return make_row(converted_data)


def load_peaks_from_hdf5(data) -> Dict[int, np.ndarray]:
    """
    Load the peaks event times for each electrode
    Meant to be used only from load_phase_from_hdf5 function
    @param [in] data: the HDF5 data struct
    @returns a map {electrode_index -> array of times}
    """
    InfoTimeStamp = data['InfoTimeStamp']

    indices = []
    map: Dict[int, int] = {}
    # here we construct a map from the position of an electrode in the array
    # and its actual name (label)
    for el in InfoTimeStamp[:]:
        indices.append(el[0])
        map[el[0]] = el[2]

    ret: Dict[int, np.ndarray] = {}

    for entry in data.keys():
        if entry.startswith('TimeStampEntity_'):
            index = int(entry[16:])
            ret[map[index]] = np.array(data[f'TimeStampEntity_{index}'])[0]

    return ret


def load_digital_from_hdf5(data) -> Signal:
    """
    Extract the digital signal from an hdf5 file.
    Meant to be used only from load_phase_from_hdf5 function
    @param [in] data: the HDF5 data struct
    @returns the digital Signal
    """

    InfoChannel = data['InfoChannel']
    data_index = 0
    sampling_frequency: float = 1e6 / \
        InfoChannel[data_index][9]  # TODO check correct index

    ChannelData = data['ChannelData']
    signal_data = ChannelData[data_index]
    signal_data -= np.min(signal_data)

    return Signal(signal_data, sampling_frequency)


def load_phase_from_hdf5(filename: Path,
                         info: Optional[PhaseInfo] = None) -> Phase:
    """
    Build a Phase instance from an HDF5 file and some metadata.
    @param [in] filename: the path of the HDF5 file
    @param [in] info: a custom PhaseInfo if the name of the file does not
                      respect the name convention (see the documentation of
                      PhaseInfo for the details. This, however does not
                      prevent from using the default parsing and adding
                      information to it.
    @returns a Phase instance

    An example of customizing the default parsing could be:

    filename = Path(phase_file)
    info = PhaseInfo().default_parse(filename)
    phase = load_phase_from_hdf5(filename, info)
    """

    if info is not None:
        pass
    else:
        info = PhaseInfo().default_parse(Path(filename))

    data = File(filename)['/Data/Recording_0']

    # checks if the data has a digital signal and the phase info too
    if info.digital and len(data['AnalogStream']) == 1:
        raise Exception("info.digital is True but the phase does not contain"
                        " two Analog Streams")
    digital = load_digital_from_hdf5(
        data['AnalogStream/Stream_0/']) if info.digital\
        else None

    return Phase(info.name,
                 peaks=load_peaks_from_hdf5(
                     data['TimeStampStream/Stream_0']),
                 digital=digital,
                 sampling_frequency=info.sampling_frequency,
                 durate=0,  # info.durate, # TODO compute durate from hdf5
                 )


def load_experiment_from_hdf5_files(path_list: List[Path],
                                    info_list: Optional[Dict[Path, PhaseInfo]]
                                    = None) -> Experiment:
    """
    Build an experiment instance from a list of files that contain its phases.
    @param [in] path_list: list of path of the phases files
    @param [in] info_list: map from a file path to it's phase's info
    @returns the converted experiment

    A possible usage is to get all h5 files from a directory and, if the names
    respect the naming convention, let the default parse get the metadata:

    from os import listdir
    from pathlib import Path

    path_list = []
    files = listdir(phases_path)
    for file in files:
        if file.ends_with('.h5'):
            path_list.append(Path(file))
    exp = load_experiment_from_hdf5_files(path_list)
    """

    phases = []
    for path in path_list:
        if not path.exists():
            raise (f'ERROR: load_experiment_from_hdf5_files. Some {path} does'
                   'not exists')
        phases.append(load_phase_from_hdf5(
            path,
            info_list[Path] if info_list is not None else None))
