import os
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

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


def save_freq_res(data: np.ndarray, ref_data: np.ndarray, fig_path: str, title='Frequency Response', channel='All'):
    """

    :param fig_path:
    :param data:
    :param ref_data:
    :param title:
    """
    plt.figure()
    plt.semilogx(ref_data[:, 0], ref_data[:, 1], label='Reference')
    plt.semilogx(data[:, 0], data[:, 1], '-.', label='Measured')
    if channel == 'WF':
        plt.xlim(10, 400)
        plt.ylim(-40, -10)
    elif channel == 'TW':
        plt.xlim(3_000, 40_000)
        plt.ylim(-40, -20)
    elif channel == 'MR':
        plt.xlim(200, 5_000)
        plt.ylim(-40, -10)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('RMS Level [dBFS]')
    plt.title(title)
    plt.legend()
    plt.grid()
    plt.savefig(fig_path)
    plt.close()


def load_csv(file_path: str, file_name: str):
    """
    Load .csv file and return it as a numpy array.
    :return:
    data (np.ndarray): data contained in the .csv file.
    """
    file = file_path + '\\' + file_name
    with open(file) as f:
        data = list(csv.reader(f, delimiter=";"))

    return np.array(data)


def print_csv(file_path: str, file_name: str):
    """
    Load .csv file and return it as a numpy array.
    :return:
    data (np.ndarray): data contained in the .csv file.
    """
    file = file_path + '\\' + file_name
    with open(file) as f:
        data = list(csv.reader(f, delimiter=";"))

    print(data)


def get_freq_res(project: str, channel: list[str]):
    """
    Measure the frequency response of the DUT and return as a np.ndarray.

    :param channel:
    :param project:
    """
    # Initialize APx
    APx = APx500_Application()
    # Load project template
    APx.OpenProject(project)
    # Run APx file
    APx.Sequence.Run()

    x_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetXValues(
        channel, VerticalAxis.Left, SourceDataType.Measured, 1)
    y_values = APx.Sequence[0]['Acoustic Response'].SequenceResults['RMS Level'].GetYValues(
        channel, VerticalAxis.Left, SourceDataType.Measured, 1)

    rms_level = np.array([x_values, y_values]).T

    data = {'rms_level': rms_level}

    return data


def get_delay(project: str, channel: list[str]):
    """
    Measure the frequency response of the DUT and return as a np.ndarray.

    :param channel:
    :param project:
    """
    # Initialize APx
    APx = APx500_Application()
    # Load project template
    APx.OpenProject(project)
    # Run APx file
    APx.Sequence.Run()

    ch_delay = np.array(APx.Sequence[0]['Acoustic Response'].SequenceResults['Delay'].GetMeterValues())

    data = {'channel_delay': ch_delay}

    return data


def check_limits(data: np.ndarray, ref_data: np.ndarray, start_frequency: float, end_frequency: float,
                 tolerance: float):
    """
    Compares the arrays of data and ref_data. Returns True, if the difference between the values in the second column
    are within the tolerance. Returns False if not and prints a graph with the data and upper/lower data limits as well
    as the points where data exceeds the limits. Pass tests can return a plot when 'plot_pass' is set to true.

    Args:
        data (ndarray):
        ref_data (ndarray):
        start_frequency (float):
        end_frequency (float):
        tolerance (float):
        plot_pass (bool, default=False):

    Returns:
        [type]: [description]
        :type tolerance: object
        :param tolerance:
        :param end_frequency:
        :param start_frequency:
        :param ref_data:
        :param data:
    """
    idx_L = np.where(ref_data[:, 0] >= start_frequency)[0][0]
    idx_H = np.where(ref_data[:, 0] >= end_frequency)[0][0]

    data = data[idx_L:idx_H, :]
    ref_data = ref_data[idx_L:idx_H, :]

    # Check if frequency vectors are equal:
    assert data[:, 0].shape[0] == ref_data[:, 0].shape[0], 'Different input shapes'

    abs_error = np.abs(ref_data[:, 1] - data[:, 1])

    if np.max(abs_error) <= tolerance:
        return True
    else:
        return False
