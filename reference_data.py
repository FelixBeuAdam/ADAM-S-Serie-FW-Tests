import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import helpers

matplotlib.use('TkAgg')

# AP Imports
import clr

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

# Add a reference to the APx API
clr.AddReference(r'C:\\Program Files\\Audio Precision\\APx500 9.0\\API\\AudioPrecision.API2.dll')
clr.AddReference(r'C:\\Program Files\\Audio Precision\\APx500 9.0\\API\\AudioPrecision.API.dll')

# noinspection PyUnresolvedReferences
from AudioPrecision.API import *

# get project path from main entry file
FILE_PATH = os.path.dirname(os.path.abspath(__name__))
REF_DATA_PATH = os.path.join(FILE_PATH, 'Reference Data')
AP_SEQ_FREQUENCY_RESPONSE_XLR = os.path.join(FILE_PATH, 'AP Sequences\\Frequency_Response_XLR.approjx')

# Channel Index
CH_IDX = [InputChannelIndex.Ch1, InputChannelIndex.Ch2, InputChannelIndex.Ch3]

S_SERIE_MODELS = ['S2V', 'S3V', 'S3H', 'S5V', 'S5H']
S_SERIE_PRESETS = ['PURE', 'UNR', 'USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5']
CHANNELS = {'S2V': ['WF', 'TW'], 'S3V': ['WF', 'TW', 'MR'], 'S3H': ['WF', 'TW', 'MR'], 'S5V': ['WF', 'TW', 'MR'],
            'S5H': ['WF', 'TW', 'MR']}
SHELVING_FILTERS = ['-12', '-6', '+6', '+12']


def measure_freq_res_xlr(path: str, channel: list[str], preset: str):
    """

    :param preset:
    :param channel:
    :type path: object
    """
    # Initialize APx
    APx = APx500_Application()
    # Load project template
    APx.OpenProject(AP_SEQ_FREQUENCY_RESPONSE_XLR)
    # Run APx file
    APx.Sequence.Run()
    # Save curve to file
    for idx in range(len(channel)):
        name = 'Ref_Freq_Res_' + preset + '_' + channel[idx] + '_dBFS.csv'
        delay_name = 'Ref_Delay_' + preset + '_' + channel[idx] + '_s.csv'
        file = os.path.join(path, name)
        delay_file = os.path.join(path, delay_name)
        x_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetXValues(
            CH_IDX[idx], VerticalAxis.Left, SourceDataType.Measured, 1)
        y_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetYValues(
            CH_IDX[idx], VerticalAxis.Left, SourceDataType.Measured, 1)
        rms_level = np.array([x_values, y_values]).T
        # Save Frequency Response to file
        np.savetxt(file, rms_level, delimiter=';')
        # Save Delay to file
        delay = np.array(APx.Sequence[0]['Acoustic Response'].SequenceResults['Delay'].GetMeterValues()[idx])
        delay.tofile(delay_file, sep=';')


if __name__ == "__main__":
    MODEL = input('Enter the DUT model: ')
    assert MODEL in S_SERIE_MODELS, 'Unrecognized S-Serie model'
    PRESET = input('Enter the DUT preset: ')
    assert PRESET in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
    if ' ' in PRESET:
        PRESET = PRESET.replace(' ', '_')

    file_path = os.path.join(REF_DATA_PATH, MODEL)
    measure_freq_res_xlr(file_path, CHANNELS[MODEL], PRESET)

    measure = input('Would you like to continue the measurement process [y/n]: ')
    assert measure in ['y', 'n'], 'Unrecognized input argument'
    while measure != 'n':
        PRESET = input('Enter the DUT preset: ')
        assert PRESET in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        measure_freq_res_xlr(file_path, CHANNELS[MODEL], PRESET)
        measure = input('Would you like to continue the measurement process [y/n]: ')
        assert measure in ['yes', 'no', 'Yes', 'No', 'YES', 'NO'], 'Unrecognized input argument'

    measure = input('Would you like to proceed with shelving filter measurements [y/n]: ')
    assert measure in ['y', 'n'], 'Unrecognized input argument'

    if measure == 'y':
        PRESET = input('Enter the DUT preset: ')
        assert PRESET in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        if ' ' in PRESET:
            PRESET = PRESET.replace(' ', '_')
        for i in range(len(SHELVING_FILTERS)):
            print('Set the DUT Lo-Shelf and Hi-Shelf to ' + SHELVING_FILTERS[i] + ' dB')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                shelving_preset = PRESET + '_' + SHELVING_FILTERS[i] + 'dB'
                measure_freq_res_xlr(file_path, CHANNELS[MODEL], shelving_preset)
