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
PROJECT_PATH = os.path.dirname(os.path.abspath(__name__))
REF_DATA_PATH = os.path.join(PROJECT_PATH, 'Reference Data')
LOG_PATH = os.path.join(PROJECT_PATH, 'Log')
AP_SEQ_FREQUENCY_RESPONSE_XLR = os.path.join(PROJECT_PATH, 'AP Sequences\\Frequency_Response_XLR.approjx')

MODEL = 'S2V'
FILE_PATH = os.path.join(REF_DATA_PATH, MODEL)
PASS_PATH = os.path.join(LOG_PATH, MODEL) + '\\Pass\\'
FAIL_PATH = os.path.join(LOG_PATH, MODEL) + '\\Fail\\'


# @pytest.mark.xray('AS-87')
def test_frequency_response_pure_wf():
    """
        AS-87 Frequency Response Pure
        :return:
    """
    CHANNEL = 'WF'
    file_name = 'Ref_Freq_Res_' + CHANNEL + '_dBFS.csv'
    reference_data = (helpers.load_csv(FILE_PATH, file_name))[4:].astype(float)
    measured_data = helpers.get_freq_res_xlr(AP_SEQ_FREQUENCY_RESPONSE_XLR)

    data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                               start_frequency=10, end_frequency=10_000, tolerance=0.1))
    if data_within_limits:
        pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_WF_PASS.png'
        helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                              title='AS-87: Frequency Response Pure - Woofer Channel')
    else:
        fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_WF_FAIL.png'
        helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                              title='AS-87: Frequency Response Pure - Woofer Channel')

    assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


def test_frequency_response_pure_tw():
    """
    AS-87 Frequency Response Pure
    :return:
    """
    CHANNEL = 'TW'
    file_name = 'Ref_Freq_Res_' + CHANNEL + '_dBFS.csv'
    reference_data = (helpers.load_csv(FILE_PATH, file_name))[4:].astype(float)
    measured_data = helpers.get_freq_res_xlr(AP_SEQ_FREQUENCY_RESPONSE_XLR)

    data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                               start_frequency=100, end_frequency=20_000, tolerance=0.1))
    if data_within_limits:
        pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_TW_PASS.png'
        helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                              title='AS-87: Frequency Response Pure - Tweeter Channel')
    else:
        fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_TW_FAIL.png'
        helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                              title='AS-87: Frequency Response Pure - Tweeter Channel')

    assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


def test_delay_wf():
    """
    AS-88 Woofer Channel Delay Test
    :return:
    """
    CHANNEL = 'WF'
    file_name = 'Ref_Delay_' + CHANNEL + '_ms.csv'
    reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
    measured_data = helpers.get_freq_res_xlr(AP_SEQ_FREQUENCY_RESPONSE_XLR)

    meas_ref_ratio = measured_data['channel_delay'] / reference_data[0]
    deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
    tolerance = 5  # Tolerance in percentage

    woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                    'Measured Delay': ' ' + str(measured_data['channel_delay']) + ' s',
                    'Tolerance': ' ' + str(tolerance) + ' %',
                    'Deviation': ' ' + str(deviation) + ' %'}

    if deviation <= tolerance:
        pass_txt_name = PASS_PATH + 'AS-88_Delay_WF_PASS.txt'
        with open(pass_txt_name, 'w') as f:
            for key, value in woofer_delay.items():
                f.write('%s:%s\n' % (key, value))
    else:
        fail_txt_name = FAIL_PATH + 'AS-88_Delay_WF_FAIL.txt'
        with open(fail_txt_name, 'w') as f:
            for key, value in woofer_delay.items():
                f.write('%s:%s\n' % (key, value))

    assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'


def test_delay_tw():
    """
    AS-88 Tweeter Channel Delay Test
    :return:
    """
    CHANNEL = 'TW'
    file_name = 'Ref_Delay_' + CHANNEL + '_ms.csv'
    reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
    measured_data = helpers.get_freq_res_xlr(AP_SEQ_FREQUENCY_RESPONSE_XLR)

    meas_ref_ratio = measured_data['channel_delay'] / reference_data[0]
    deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
    tolerance = 10  # Tolerance in percentage

    woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                    'Measured Delay': ' ' + str(measured_data['channel_delay']) + ' s',
                    'Tolerance': ' ' + str(tolerance) + ' %',
                    'Deviation': ' ' + str(deviation) + ' %'}

    if deviation <= tolerance:
        pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CHANNEL + '_PASS.txt'
        with open(pass_txt_name, 'w') as f:
            for key, value in woofer_delay.items():
                f.write('%s:%s\n' % (key, value))
    else:
        fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CHANNEL + '_FAIL.txt'
        with open(fail_txt_name, 'w') as f:
            for key, value in woofer_delay.items():
                f.write('%s:%s\n' % (key, value))

    assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'
