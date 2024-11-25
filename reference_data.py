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
SHELVING_CUTOFF = ['400', '5000']
CH_DELAYS = ['0', '2.5', '5']


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
        file = os.path.join(path, name)
        x_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetXValues(
            CH_IDX[idx], VerticalAxis.Left, SourceDataType.Measured, 1)
        y_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetYValues(
            CH_IDX[idx], VerticalAxis.Left, SourceDataType.Measured, 1)
        rms_level = np.array([x_values, y_values]).T
        # Save Frequency Response to file
        np.savetxt(file, rms_level, delimiter=';')


def measure_delay_xlr(path: str, channel: list[str], preset: str):
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
        delay_name = 'Ref_Delay_' + preset + '_' + channel[idx] + '_s.csv'
        delay_file = os.path.join(path, delay_name)
        # Save Delay to file
        delay = np.array(APx.Sequence[0]['Acoustic Response'].SequenceResults['Delay'].GetMeterValues()[idx])
        delay.tofile(delay_file, sep=';')


if __name__ == "__main__":
    model = input('Enter the DUT model: ')
    assert model in S_SERIE_MODELS, 'Unrecognized S-Serie model'

    file_path = os.path.join(REF_DATA_PATH, model)

    ref_meas = input('Would you like to proceed with the frequency response reference measurement [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'
    if ref_meas == 'y':
        print('Please set the DUT preset to PURE')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset != 'PURE', 'Current user preset is not set to PURE'
        measure_freq_res_xlr(file_path, CHANNELS[model], user_preset)
        print('Please set the DUT preset to UNR')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset != 'UNR', 'Current user preset is not set to UNR'
        measure_freq_res_xlr(file_path, CHANNELS[model], user_preset)

    ref_meas = input('Would you like to proceed with the DUT shelving filter reference measurements [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'
    if ref_meas == 'y':
        print('Please set the DUT preset to one of the custom USER presets')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        if ' ' in user_preset:
            user_preset = user_preset.replace(' ', '_')
        print('Please set the DUT Lo-Shelf cutoff frequency to ' + SHELVING_CUTOFF[0] + ' Hz')
        print('Please set the DUT Hi-Shelf cutoff frequency to ' + SHELVING_CUTOFF[1] + ' Hz')
        for i in range(len(SHELVING_FILTERS)):
            print('Please set the DUT Lo-Shelf and Hi-Shelf to ' + SHELVING_FILTERS[i] + ' dB')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                shelving_preset = user_preset + '_' + SHELVING_FILTERS[i] + 'dB'
                measure_freq_res_xlr(file_path, CHANNELS[model], shelving_preset)

    ref_meas = input('Would you like to proceed with the DUT delay reference measurements [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    if ref_meas == 'y':
        user_preset = input('Please enter the DUT preset: ')
        assert user_preset in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        if ' ' in user_preset:
            user_preset = user_preset.replace(' ', '_')
        for i in range(len(CH_DELAYS)):
            print('Please set the DUT delay to ' + CH_DELAYS[i] + ' ms')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                delay_preset = user_preset + '_' + CH_DELAYS[i] + 'ms'
                measure_delay_xlr(file_path, CHANNELS[model], delay_preset)

    ref_meas = input('Would you like to measure the frequency response of additional user presets? [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'
    while ref_meas != 'n':
        user_preset = input('Enter the DUT preset: ')
        assert user_preset in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        measure_freq_res_xlr(file_path, CHANNELS[model], user_preset)
        ref_meas = input('Would you like to continue the measurement process [y/n]: ')
        assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    print('Thank you very much for performing the S-Serie reference data measurements, have a nice day.')
