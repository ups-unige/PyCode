from pathlib import Path
from pycode.io import load_raw_signal_from_hdf5
from pycode.operation import filter_signal, spike_detection
from h5py import File

import numpy as np
import matplotlib.pyplot as plt

# take an electrode number
ELECTRODE_NUMBER = 0
MC_ELECTRODE_NUMBER = ELECTRODE_NUMBER

def test_sd():
    # load data
    sd_data_path = Path('E:/unige/PyCode/tests/experimenter_test/raw.h5')
    sd_data_el = load_raw_signal_from_hdf5(sd_data_path, ELECTRODE_NUMBER, debug=True)
    # filter it
    filtered_data = filter_signal(sd_data_el, 10e3, 70)
    # spike detection
    sd_ts = spike_detection(filtered_data)[1]
    sd_ts = sd_ts[np.where(sd_ts != 0)]

    # load spike detection mc
    mc_sd_path = Path('E:/unige/PyCode/tests/experimenter_test/raw.h5')
    mc_sd_data = File(mc_sd_path, 'r')

    # manage to extrapolate spike times
    print(mc_sd_data['/Data/Recording_0/TimeStampStream/Stream_0/InfoTimeStamp'][MC_ELECTRODE_NUMBER])
    mc_sd_ts = mc_sd_data[f'/Data/Recording_0/TimeStampStream/Stream_0/TimeStampEntity_{MC_ELECTRODE_NUMBER}'][0]/100

    # plot both spike trains
    print(sd_ts)
    print(mc_sd_ts)
    sd_ts_shape = np.shape(sd_ts)
    mc_sd_ts_shape = np.shape(mc_sd_ts)

    plt.stem(sd_ts, np.ones(shape=sd_ts_shape))
    plt.stem(mc_sd_ts, -np.ones(shape=mc_sd_ts_shape))
    plt.show()

if __name__ == '__main__':
    test_sd()
