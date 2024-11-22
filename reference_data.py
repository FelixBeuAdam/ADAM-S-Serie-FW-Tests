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
    for i in range(len(channel)):
        name = 'Ref_Freq_Res_' + preset + '_' + channel[i] + '_dBFS.csv'
        delay_name = 'Ref_Delay_' + preset + '_' + channel[i] + '_s.csv'
        file = os.path.join(path, name)
        delay_file = os.path.join(path, delay_name)
        x_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetXValues(
            CH_IDX[i], VerticalAxis.Left, SourceDataType.Measured, 1)
        y_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetYValues(
            CH_IDX[i], VerticalAxis.Left, SourceDataType.Measured, 1)
        rms_level = np.array([x_values, y_values]).T
        # Save Frequency Response to file
        np.savetxt(file, rms_level, delimiter=';')
        # Save Delay to file
        delay = np.array(APx.Sequence[0]['Acoustic Response'].SequenceResults['Delay'].GetMeterValues()[i])
        delay.tofile(delay_file, sep=';')


if __name__ == "__main__":
    s_serie_models = ['S2V', 'S3V', 'S3H', 'S5V', 'S5H']
    s_serie_presets = ['PURE', 'UNR', 'USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5']

    MODEL = input('Enter the DUT model: ')
    assert MODEL in s_serie_models, 'Unrecognized S-Serie model'
    PRESET = input('Enter the DUT preset: ')
    assert PRESET in s_serie_presets, 'Unrecognized S-Serie preset'

    CHANNELS = {'S2V': ['WF', 'TW'], 'S3V': ['WF', 'TW', 'MR'], 'S3H': ['WF', 'TW', 'MR'],
                'S5V': ['WF', 'TW', 'MR'], 'S5H': ['WF', 'TW', 'MR']}

    file_path = os.path.join(REF_DATA_PATH, MODEL)
    measure_freq_res_xlr(file_path, CHANNELS[MODEL], PRESET)
