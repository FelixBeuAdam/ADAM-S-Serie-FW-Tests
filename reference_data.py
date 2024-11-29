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
AP_SEQ_FREQUENCY_RESPONSE_AES3 = os.path.join(FILE_PATH, 'AP Sequences\\Frequency_Response_AES3.approjx')

# Channel Index
CH_IDX = [InputChannelIndex.Ch1, InputChannelIndex.Ch2, InputChannelIndex.Ch3]

S_SERIE_MODELS = ['S2V', 'S3V', 'S3H', 'S5V', 'S5H']
S_SERIE_PRESETS = ['PURE', 'UNR', 'USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5']
CHANNELS = {'S2V': ['WF', 'TW'], 'S3V': ['WF', 'TW', 'MR'], 'S3H': ['WF', 'TW', 'MR'], 'S5V': ['WF', 'TW', 'MR'],
            'S5H': ['WF', 'TW', 'MR']}
SHELVING_FILTERS = ['-12', '-6', '+6', '+12']
SHELVING_CUTOFF = ['400', '5000']
CH_DELAYS = ['0', '2.5', '5']
VOLUME = ['-60', '-12', '-6', '0', '+6', '+12']
CUSTOM_EQS = 6
SAMPLE_RATES = ['44_100', '48_000', '88_200', '96_000', '176_400', '192_000']
DEVICE_INPUT = ['Analog', 'AESL', 'AESR']


def measure_freq_res(path: str, channel: list[str], preset: str, ap_sequence=AP_SEQ_FREQUENCY_RESPONSE_XLR):
    """

    :param ap_sequence:
    :param preset:
    :param channel:
    :type path: object
    """
    # Initialize APx
    APx = APx500_Application()
    # Load project template
    APx.OpenProject(ap_sequence)
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


def random_eq_settings(path: str, preset: str, eq_slots: int):
    """

    :param path:
    :param eq_slots:
    :return:
    """
    eq_settings = []

    for idx in range(eq_slots):
        if idx < eq_slots // 2:
            eq = str(np.random.randint(20, 1_000))
        else:
            eq = str(np.random.randint(1_000, 20_000))
        q = str(np.round(np.random.uniform(0.1, 20), 1))
        db = str(np.round(np.random.uniform(-12, 12), 1))
        eq_settings.append({'EQ': eq, 'Q': q, 'dB': db})

    settings_name = 'REF_Custom_EQ_' + preset + '_Settings.csv'
    settings_file = os.path.join(path, settings_name)
    with open(settings_file, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['EQ', 'Q', 'dB'])
        writer.writeheader()
        writer.writerows(eq_settings)

    return eq_settings


if __name__ == "__main__":
    model = input('Please enter the DUT model: ')
    assert model in S_SERIE_MODELS, 'Unrecognized S-Serie model'

    file_path = os.path.join(REF_DATA_PATH, model)

    ref_meas = input('Would you like to proceed with the frequency response reference measurements [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'
    if ref_meas == 'y':
        print('Please set the DUT preset to PURE')
        proceed_meas = input('Confirm measurement [y/n]: ')
        if proceed_meas == 'y':
            for inpt in range(len(DEVICE_INPUT)):
                print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                dev_preset = input('Please confirm the current DUT input: ')
                assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                for i in range(len(VOLUME)):
                    print('Please set the DUT volume to ' + VOLUME[i] + ' dB')
                    proceed_meas = input('Confirm measurement [y/n]: ')
                    if proceed_meas == 'y':
                        volume_preset = 'PURE_' + VOLUME[i] + 'dB_' + DEVICE_INPUT[inpt]
                        measure_freq_res(file_path, CHANNELS[model], volume_preset)
        print('Please set the DUT volume to 0 dB')
        print('Please set the DUT preset to UNR')
        proceed_meas = input('Confirm measurement [y/n]: ')
        if proceed_meas == 'y':
            for inpt in range(len(DEVICE_INPUT)):
                print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                dev_preset = input('Please confirm the current DUT input: ')
                assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                unr_preset = 'UNR_0dB_' + DEVICE_INPUT[inpt]
                measure_freq_res(file_path, CHANNELS[model], unr_preset)

    ref_meas = input('Would you like to proceed with the DUT shelving filter reference measurements [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    if ref_meas == 'y':
        print('Please set the DUT preset to the custom USER 1 preset')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset == 'USER 1', 'Current user preset is not set to USER 1'
        if ' ' in user_preset:
            user_preset = user_preset.replace(' ', '_')
        print('Please set the DUT Lo-Shelf cutoff frequency to ' + SHELVING_CUTOFF[0] + ' Hz')
        print('Please set the DUT Hi-Shelf cutoff frequency to ' + SHELVING_CUTOFF[1] + ' Hz')
        for i in range(len(SHELVING_FILTERS)):
            print('Please set the DUT Lo-Shelf and Hi-Shelf gain to ' + SHELVING_FILTERS[i] + ' dB')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                for inpt in range(len(DEVICE_INPUT)):
                    print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                    dev_preset = input('Please confirm the current DUT input: ')
                    assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                    shelving_preset = user_preset + '_' + DEVICE_INPUT[inpt] + '_' + SHELVING_FILTERS[i] + 'dB'
                    measure_freq_res(file_path, CHANNELS[model], shelving_preset)

    ref_meas = input('Would you like to proceed with the DUT custom EQ reference measurements [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    if ref_meas == 'y':
        print('Please set the DUT preset to the custom USER 2 preset')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset == 'USER 2', 'Current user preset is not set to USER 2'
        if ' ' in user_preset:
            user_preset = user_preset.replace(' ', '_')
        custom_eqs = random_eq_settings(path=file_path, preset=user_preset, eq_slots=CUSTOM_EQS)
        print('Please set the DUT custom EQ with the following settings: ')
        for i in range(CUSTOM_EQS):
            print(custom_eqs[i])
        print('NOTE: Please choose the closest available center frequency/Q value if the firmware version does not'
              ' support arbitrary selection.')
        proceed_meas = input('Confirm measurement [y/n]: ')
        if proceed_meas == 'y':
            for inpt in range(len(DEVICE_INPUT)):
                print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                dev_preset = input('Please confirm the current DUT input: ')
                assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                eq_preset = user_preset + '_' + dev_preset
                measure_freq_res(file_path, CHANNELS[model], user_preset)

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
                for inpt in range(len(DEVICE_INPUT)):
                    print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                    dev_preset = input('Please confirm the current DUT input: ')
                    assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                    delay_preset = user_preset + '_' + CH_DELAYS[i] + 'ms_' + DEVICE_INPUT[inpt]
                    measure_delay_xlr(file_path, CHANNELS[model], delay_preset)

    ref_meas = input('Would you like to proceed with the AES3 input measurements? [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    if ref_meas == 'y':
        print('Please set the DUT preset to PURE')
        user_preset = input('Please confirm the current DUT preset: ')
        assert user_preset == 'PURE', 'Current user preset is not set to PURE'
        for i in range(len(SAMPLE_RATES)):
            print('Please set the sample rate in the output configuration to ' + SAMPLE_RATES[i]
                  + ' Hz and save the file')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                for inpt in range(1, len(DEVICE_INPUT)):
                    print('Please set the DUT input to ' + DEVICE_INPUT[inpt])
                    dev_preset = input('Please confirm the current DUT input: ')
                    assert dev_preset == DEVICE_INPUT[inpt], 'Current DUT input is not set to ' + DEVICE_INPUT[inpt]
                    sample_rate_preset = user_preset + '_' + SAMPLE_RATES[i] + 'Hz_' + DEVICE_INPUT[inpt]
                    measure_freq_res(file_path, CHANNELS[model], sample_rate_preset,
                                     ap_sequence=AP_SEQ_FREQUENCY_RESPONSE_XLR)

    ref_meas = input('Would you like to measure the frequency response of additional user presets? [y/n]: ')
    assert ref_meas in ['y', 'n'], 'Unrecognized input argument'
    while ref_meas != 'n':
        user_preset = input('Enter the DUT preset: ')
        assert user_preset in S_SERIE_PRESETS, 'Unrecognized S-Serie preset'
        measure_freq_res(file_path, CHANNELS[model], user_preset)
        ref_meas = input('Would you like to continue the measurement process [y/n]: ')
        assert ref_meas in ['y', 'n'], 'Unrecognized input argument'

    print('Thank you very much for performing the S-Serie reference data measurements, have a nice day.')
