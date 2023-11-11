'''
Manage the MultiChannel hdf5 organization of data in the PyCode way
the specification of the hdf5 structure used by MultiChannel System
can be found at
https://www.multichannelsystems.com/sites/multichannelsystems.com/files/documents/manuals/HDF5%20MCS%20Raw%20Data%20Definition.pdf
'''

from typing import List, Dict
from pathlib import Path
from h5py import File, Group, Dataset
import numpy as np


class InfoChannel:
    def __init__(self, info_data: Dataset):
        self.who_knows = info_data[0]
        self.channel_id = info_data[1]
        self.row_index = info_data[2]
        self.group_id = info_data[3]
        self.label = info_data[4]
        self.raw_data_type = info_data[5]
        self.unit = info_data[6]
        self.exponent = info_data[7]
        self.adc_offset = info_data[8]
        self.tick = info_data[9]
        self.conversion_factor = info_data[10]
        self.adc_bits = info_data[11]
        self.highpass_type = info_data[12]
        self.highpass_cutoff = info_data[13]
        self.highpass_order = info_data[14]
        self.lowpass_type = info_data[15]
        self.lowpass_cutoff = info_data[16]
        self.lowpass_order = info_data[17]

    def __str__(self):
        return f'''
channel id:         {self.channel_id}
label:              {self.label}
raw_data_type:      {self.raw_data_type}
exponent:           {self.exponent}
unit:               {self.unit}
offset:             {self.ad_zero}
tick:               {self.tick}
conversion factor:  {self.conversion_factor}
        '''


class AnalogStream:
    def __init__(self, base_group: Group, key: str):
        self.name = key
        stream_group = base_group[key]
        try:
            self.length = stream_group['InfoChannel'].shape[0]
            self.info_channels: List[InfoChannel] = []
            for i in range(self.length):
                self.info_channels.append(
                    InfoChannel(stream_group['InfoChannel'][i]))
            self.data_channels = stream_group['ChannelData']
        except Exception as e:
            print(
                f'ERROR: AnalogStream __init__, {key} could be corrupted',
                e.args)

    def quick_info_list(self, index: int) -> List[Dict[str, str]]:
        info_channel = self.info_channels[index]
        return {
            'index': str(info_channel.channel_id),
            'label': str(info_channel.label),
        }

    def parse_signal(self, index: int) -> np.ndarray:
        print(self.info_channels)
        info_channel = self.info_channels[index]
        offset = info_channel.adc_offset
        conversion_factor = info_channel.conversion_factor
        exponent = info_channel.exponent
        mantissas = np.expand_dims(self.data_channels[index][:], 1)

        print('here 1')
        converted_data = (mantissas-np.ones(shape=mantissas.shape)*offset) *\
            conversion_factor * np.power(10., exponent)
        print('here 2')

        return converted_data

    def __str__(self):
        return f'''
Name:                   {self.name}
Number of channels:     {self.length}
        '''


class InfoTimeStamp:
    def __init__(self, info_time_stamp: np.void):
        self.channel_id = info_time_stamp[0]
        self.group = info_time_stamp[1]
        self.label = info_time_stamp[2]
        self.unit = info_time_stamp[3]
        self.exponent = info_time_stamp[4]
        self.source_id = info_time_stamp[5]
        self.source_label = info_time_stamp[6]

    def __str__(self):
        return f'''
id:                 {self.channel_id}
group:              {self.group}
label:              {self.unit}
unit:               {self.unit}
exponent:           {self.exponent}
source id:          {self.source_id}
source label:       {self.source_label}
        '''


class TimeStampStream:
    def __init__(self, base_group: Group, key: str):
        self.name = key
        stream_group = base_group[key]
        try:
            info_time_stamps = stream_group['InfoTimeStamp']
            self.info_time_stamps = []
            self.length = info_time_stamps.shape[0]
            for i in range(self.length):
                self.info_time_stamps.append(
                    InfoTimeStamp(info_time_stamps[i]))
                print(self.info_time_stamps[i])
        except Exception as e:
            print(
                f'ERROR: TimeStampStream __init__, {key} could be corrupted',
                e.args)

    def quick_info_list(self, index: int) -> List[Dict[str, str]]:
        info_time_stamp = self.info_time_stamps[index]
        return {
            'index': str(info_time_stamp.channel_id),
            'label': str(info_time_stamp.label),
        }

    def __str__(self):
        return f'''
Name:                   {self.name}
Number of channels:     {self.length}
        '''


class H5Content:
    def __init__(self, filepath: Path):
        self.name = str(filepath.name)
        try:
            filepath = Path(filepath)
        except Exception as e:
            print(
                'ERROR: H5Content __init__, filepath should be a Path and is ',
                type(filepath), '\n', e)

        try:
            data = File(filepath)
            data = data['/Data/Recording_0']
            keys = data.keys()
            if 'AnalogStream' in keys:
                self.analogs = []
                analog_group = data['AnalogStream']
                analog_keys = analog_group.keys()
                for key in analog_keys:
                    self.analogs.append(AnalogStream(analog_group, key))

            else:
                self.analogs = None

            if 'TimeStampStream' in keys:
                self.time_stamps = []
                time_stamps_group = data['TimeStampStream']
                time_stamps_keys = time_stamps_group.keys()
                for key in time_stamps_keys:
                    self.time_stamps.append(
                        TimeStampStream(time_stamps_group, key))
            else:
                self.time_stamps = None

            # TODO if needed implement FrameStream, SegmentStream and
            # EventStream
            self.frames = None
            self.segments = None
            self.event = None

        except Exception as e:
            print(
                f'ERROR: H5Contnt __init__, {filepath} is maybe corrupted',
                e.args)

    def __str__(self):
        return f'''
AnalogStreams: {len(self.analogs)}
TimeStampStreams: {len(self.time_stamps)}
        '''
