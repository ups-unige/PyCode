from h5py import File
from pathlib import Path
from pycode.utils import make_fake_digital
from matplotlib import pyplot as plt

orig_h5_path = Path(
    'e:/unige/PyCode/tests/data/experimenter_test/00000_DIV40_Stim_1_60.h5')

new_h5_path = Path(
    'e:/unige/PyCode/tests/data/experimenter_test/'
    '00000_DIV40_Stim_1_60__with_digital.h5')


if __name__ == "__main__":
    with File(orig_h5_path, 'a') as orig:
        n_samples = orig['/Data/Recording_0/AnalogStream/'
                         'Stream_0/ChannelData'].shape[1]

        del orig['/Data/Recording_0/AnalogStream/Stream_0/ChannelData']
        orig['/Data/Recording_0/AnalogStream/Stream_0/ChannelData'] =\
            make_fake_digital(n_samples/10000, 0.250, 4., 0.).astype(int)

        plt.plot(orig['/Data/Recording_0/AnalogStream/Stream_0/ChannelData']
                 [0])
        plt.show()
