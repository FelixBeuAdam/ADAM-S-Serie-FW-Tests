import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import helpers
import pytest

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
AP_SEQ_FREQUENCY_RESPONSE_AES3 = os.path.join(PROJECT_PATH, 'AP Sequences\\Frequency_Response_AES3.approjx')

MODEL = 'S2V'
FILE_PATH = os.path.join(REF_DATA_PATH, MODEL)
PASS_PATH = os.path.join(LOG_PATH, MODEL) + '\\Pass\\'
FAIL_PATH = os.path.join(LOG_PATH, MODEL) + '\\Fail\\'

CH_IDX = [InputChannelIndex.Ch1, InputChannelIndex.Ch2, InputChannelIndex.Ch3]
CHANNEL = ['WF', 'TW', 'MR']

S_SERIE_MODELS = ['S2V', 'S3V', 'S3H', 'S5V', 'S5H']
S_SERIE_PRESETS = ['PURE', 'UNR', 'USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5']
CHANNELS = {'S2V': ['WF', 'TW'], 'S3V': ['WF', 'TW', 'MR'], 'S3H': ['WF', 'TW', 'MR'], 'S5V': ['WF', 'TW', 'MR'],
            'S5H': ['WF', 'TW', 'MR']}
SHELVING_FILTERS = ['-12', '-6', '+6', '+12']
SHELVING_CUTOFF = ['400', '5000']
CH_DELAYS = ['0ms', '2.5ms', '5ms']
VOLUME = ['-60dB', '-12dB', '-6dB', '0dB', '+6dB', '+12dB']
CUSTOM_EQS = 6
SAMPLE_RATES = ['44_100', '48_000', '88_200', '96_000', '176_400', '192_000']


# @pytest.mark.test_key('AS-87')
@pytest.mark.parametrize('dut_input', ['XLR', 'AESL', 'AESR'])
class TestFrequencyResponsePURE:
    def test_frequency_response_pure_wf(self, dut_input):
        """
            AS-87 Frequency Response Pure
            :return:

        Parameters
        ----------
        CHANNEL
        """
        file_name = 'Ref_Freq_Res_PURE_0dB_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_PURE_WF_' + dut_input + '_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-87: Frequency Response PURE - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_PURE_WF_' + dut_input + '_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response PURE - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    def test_frequency_response_pure_tw(self, dut_input):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        file_name = 'Ref_Freq_Res_PURE_0dB_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_PURE_TW_' + dut_input + '_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-87: Frequency Response PURE - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_PURE_TW_' + dut_input + '_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response PURE - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    @pytest.mark.skipif(MODEL == 'S2V', reason='Selected model does not have a midrange channel')
    def test_frequency_response_pure_mr(self, dut_input):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        file_name = 'Ref_Freq_Res_PURE_0dB_' + CHANNEL[2] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[2])

        data_within_limits = (helpers.check_limits(data=self.measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=300, end_frequency=6_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_PURE_MR_' + dut_input + '_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-87: Frequency Response PURE - Midrange Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_PURE_MR_' + dut_input + '_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response PURE - Midrange Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


class TestDelay:

    # @pytest.mark.xray('AS-88')
    def test_delay_0_ms_wf(self):
        """
        AS-88 Woofer Channel Delay Test
        :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[0] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
        meas_ref_ratio = measured_data['channel_delay'][0] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][0]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[0] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[0] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.xray('AS-88')
    def test_delay_0ms_tw(self):
        """
        AS-88 Tweeter Channel Delay Test
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[0] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        meas_ref_ratio = measured_data['channel_delay'][1] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][1]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %',
                        'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[0] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[0] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.xray('AS-88')
    def test_delay_2_5ms_wf(self):
        """
        AS-88 Woofer Channel Delay Test
        :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[1] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
        meas_ref_ratio = measured_data['channel_delay'][0] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][0]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[1] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[1] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.xray('AS-88')
    def test_delay_2_5ms_tw(self):
        """
        AS-88 Tweeter Channel Delay Test
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[1] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        meas_ref_ratio = measured_data['channel_delay'][1] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][1]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %',
                        'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[1] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[1] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.xray('AS-88')
    def test_delay_5ms_wf(self):
        """
        AS-88 Woofer Channel Delay Test
        :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[2] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
        meas_ref_ratio = measured_data['channel_delay'][0] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][0]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[2] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[2] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.xray('AS-88')
    def test_delay_5ms_tw(self):
        """
        AS-88 Tweeter Channel Delay Test
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Delay_PURE_' + CH_DELAYS[2] + '_' + CHANNEL + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        meas_ref_ratio = measured_data['channel_delay'][1] / reference_data[0]
        deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
        tolerance = 5  # Tolerance in percentage

        woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                        'Measured Delay': ' ' + str(measured_data['channel_delay'][1]) + ' s',
                        'Tolerance': ' ' + str(tolerance) + ' %',
                        'Deviation': ' ' + str(deviation) + ' %'}

        if deviation <= tolerance:
            pass_txt_name = PASS_PATH + 'AS-88_Delay_' + CH_DELAYS[2] + '_' + CHANNEL + '_PASS.txt'
            with open(pass_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))
        else:
            fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + CH_DELAYS[2] + '_' + CHANNEL + '_FAIL.txt'
            with open(fail_txt_name, 'w') as f:
                for key, value in woofer_delay.items():
                    f.write('%s:%s\n' % (key, value))

        assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'


class TestFrequencyResponseUNR:

    # @pytest.mark.xray('AS-85')
    def test_frequency_response_unr_wf(self):
        """
            AS-85 Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_UNR_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.1))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-85_Freq_Res_UNR_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-85: Frequency Response UNR - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-85_Freq_Res_UNR_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-85: Frequency Response UNR - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-85')
    def test_frequency_response_unr_tw(self):
        """
        AS-85 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_UNR_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.1))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-85_Freq_Res_UNR_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-85: Frequency Response UNR - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-85_Freq_Res_UNR_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-85: Frequency Response UNR - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


class TestShelvingFilters:

    # @pytest.mark.xray('AS-XX')
    def test_lo_shelf_minus_12db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_USER_1_-12dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Lo_Shelf_-12dB_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf -12dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Lo_Shelf_-12dB_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf -12dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_hi_shelf_minus_12db_tw(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_USER_1_-12dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Hi_Shelf_-12dB_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf -12dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Hi_Shelf_-12dB_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf -12dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_lo_shelf_minus_6db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_USER_1_-6dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Lo_Shelf_-6dB_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf -6dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Lo_Shelf_-6dB_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf -6dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_hi_shelf_minus_6db_tw(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_USER_1_-6dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Hi_Shelf_-6dB_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf -6dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Hi_Shelf_-6dB_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf -6dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_lo_shelf_plus_6db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_USER_1_+6dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Lo_Shelf_+6dB_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf +6dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Lo_Shelf_+6dB_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf +6dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_hi_shelf_plus_6db_tw(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_USER_1_+6dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Hi_Shelf_+6dB_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf +6dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Hi_Shelf_+6dB_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf +6dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_lo_shelf_plus_12db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_USER_1_+12dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Lo_Shelf_+12dB_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf +12dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Lo_Shelf_+12dB_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Lo-Shelf +12dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_hi_shelf_plus_12db_tw(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_USER_1_+12dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_Hi_Shelf_+12dB_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf +12dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_Hi_Shelf_+12dB_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Hi-Shelf +12dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


class TestVolumeControl:

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_minus_60db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[0] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=2_000, tolerance=2.0))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[0] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -60 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[0] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -60 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_minus_60db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[0] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=3_000, end_frequency=20_000, tolerance=2.0))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[0] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -60 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[0] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -60 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_minus_12db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[1] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[1] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -12 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[1] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -12 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_minus_12db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[1] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.5))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[1] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -12 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[1] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -12 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_minus_6db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[2] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[2] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -6 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[2] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -6 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_minus_6db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[2] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[2] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -6 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[2] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ -6 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_0db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[3] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[3] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ 0 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[3] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ 0 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_0db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[3] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[3] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ 0 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[3] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ 0 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_plus_6db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[4] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[4] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +6 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[4] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +6 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_plus_6db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[4] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[4] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +6 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[4] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +6 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_volume_control_plus_12db_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[5] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[5] + '_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +12 dB - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[5] + '_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +12 dB - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_volume_control_plus_12db_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_' + VOLUME[5] + '_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[5] + '_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +12 dB - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_PURE_' + VOLUME[5] + '_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response PURE @ +12 dB - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


class TestUserEQs:

    # @pytest.mark.xray('AS-XX')
    def test_user_eqs_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_USER_2_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_USER_EQ_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Custom User EQ - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_USER_EQ_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response Custom User EQ - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_user_eqs_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_USER_2_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_USER_EQ_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response Custom User EQ - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_USER_EQ_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response Custom User EQ - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


class TestAESSampleRate:

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_44_100_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_44_100_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_44_100_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 44.1 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_44_100_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 44.1 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_44_100_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_44_100_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_44_100_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 44.1 kHz - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_44_100_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 44.1 kHz - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_48_000_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_48_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_48_000_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 48 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_48_000_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 48 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_48_000_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_48_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_48_000_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 48 kHz - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_48_000_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 48 kHz - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_96_000_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_96_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_96_000_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_96_000_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_96_000_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_96_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_96_000_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_96_000_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_176_400_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_176_400_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_176_400_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 176.4 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_176_400_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 176.4 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_176_400_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_176_400_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_176_400_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 176.4 kHz - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_176_400_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 176.4 kHz - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_192_000_wf(self):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_192_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_192_000_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 192 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_192_000_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 192 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-XX')
    def test_frequency_response_192_000_tw(self):
        """
        AS-XX Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_192_000_Hz_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_192_000_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 192 kHz - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_192_000_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 192 kHz - Tweeter Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


@pytest.mark.parametrize('channel, ch_idx, start_frequency, end_frequency',
                         [('WF', CH_IDX[0], 20, 8_000),
                          ('TW', CH_IDX[1], 100, 20_000)
                          ])
def test_frequency_response_96_000_wf(channel, ch_idx, start_frequency, end_frequency):
    """
            AS-XX Frequency Response Pure
            :return:
        """
    # CHANNEL = 'WF'
    file_name = 'Ref_Freq_Res_PURE_96_000_Hz_' + channel + '_dBFS.csv'
    reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
    print('\nPlease open the AP sequence Frequency_Response_AES3.approjx')
    print('Please set the sample rate in the output configuration to ' + SAMPLE_RATES[3] + ' Hz and save the file')
    proceed_meas = input('Would you like to proceed with the measurement? [y/n]')
    if proceed_meas == 'y':
        measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_AES3, channel=ch_idx)

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=start_frequency, end_frequency=end_frequency,
                                                   tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-XX_Freq_Res_96_000_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-XX_Freq_Res_96_000_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-XX: Frequency Response AES3 Input @ 96 kHz - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'
