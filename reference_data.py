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


def measure_freq_res_xlr(path: str, channel: str):
    """

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
    name = 'Ref_Freq_Res_' + channel + '_dBFS.csv'
    file = os.path.join(path, name)
    APx.Sequence[0]["Continuous Sweep"].SequenceResults["RMS Level"].ExportData(file)


if __name__ == "__main__":
    # Measure frequency response
    MODEL = 'S2V'
    CHANNEL = 'WF'
    file_path = os.path.join(REF_DATA_PATH, MODEL)
    measure_freq_res_xlr(file_path, CHANNEL)

    # Verify Measured Data
    file_name = 'Ref_Freq_Res_' + CHANNEL + '_dBFS.csv'
    reference_data = helpers.load_csv(file_path, file_name)
    measured_data = helpers.get_freq_res_xlr(AP_SEQ_FREQUENCY_RESPONSE_XLR)

    assert (
        helpers.check_limits(data=measured_data, ref_data=reference_data,
                             start_frequency=10, end_frequency=10_000,
                             tolerance=0.1, plot_pass=True)
    ), 'Measured frequency response is not within the specified tolerance'



