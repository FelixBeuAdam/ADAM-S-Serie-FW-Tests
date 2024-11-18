import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv

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


def measure_freq_res_xlr(file_path: str, channel: str):
    # Initialize APx
    APx = APx500_Application()
    # Load project template
    APx.OpenProject(AP_SEQ_FREQUENCY_RESPONSE_XLR)
    # Run APx file
    APx.Sequence.Run()
    # Save curve to file
    file_name = os.path.join(file_path, f'Ref_Freq_Res_{channel}_dBFS.csv')
    APx.Sequence[0]["Continuous Sweep"].SequenceResults["RMS Level"].ExportData(file_name)


if __name__ == "__main__":
    MODEL = 'S2V'
    CHANNEL = 'TW'
    file_path = os.path.join(REF_DATA_PATH, MODEL)
    measure_freq_res_xlr(file_path, CHANNEL)
    with open(
            "C:\\Users\\ADAMQA\\GitHub\\ADAM-S-Serie-FW-Regression-Tests\\Reference Data\\S2V\\"
            "Ref_Freq_Res_TW_dBFS.csv",
            'r') as x:
        sample_data = list(csv.reader(x, delimiter=";"))

    sample_data = (np.array(sample_data[4:])).astype(float)

    plt.semilogx(sample_data[:, 0], sample_data[:, 1])
    plt.grid()
    plt.show()
