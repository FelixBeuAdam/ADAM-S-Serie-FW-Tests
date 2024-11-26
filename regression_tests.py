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

CH_IDX = [InputChannelIndex.Ch1, InputChannelIndex.Ch2, InputChannelIndex.Ch3]

S_SERIE_MODELS = ['S2V', 'S3V', 'S3H', 'S5V', 'S5H']
S_SERIE_PRESETS = ['PURE', 'UNR', 'USER 1', 'USER 2', 'USER 3', 'USER 4', 'USER 5']
CHANNELS = {'S2V': ['WF', 'TW'], 'S3V': ['WF', 'TW', 'MR'], 'S3H': ['WF', 'TW', 'MR'], 'S5V': ['WF', 'TW', 'MR'],
            'S5H': ['WF', 'TW', 'MR']}
SHELVING_FILTERS = ['-12', '-6', '+6', '+12']
SHELVING_CUTOFF = ['400', '5000']
CH_DELAYS = ['0ms', '2.5ms', '5ms']
VOLUME = ['-60dB', '-12dB', '-6dB', '0dB', '+6dB', '+12dB']
CUSTOM_EQS = 6


class TestFrequencyResponsePURE:

    # @pytest.mark.xray('AS-87')
    def test_frequency_response_pure_wf(self):
        """
            AS-87 Frequency Response Pure
            :return:
        """
        CHANNEL = 'WF'
        file_name = 'Ref_Freq_Res_PURE_0dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=20, end_frequency=8_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_PURE_WF_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-87: Frequency Response PURE - Woofer Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_PURE_WF_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response PURE - Woofer Channel')

        assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.xray('AS-87')
    def test_frequency_response_pure_tw(self):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        CHANNEL = 'TW'
        file_name = 'Ref_Freq_Res_PURE_0dB_' + CHANNEL + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

        data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                   start_frequency=100, end_frequency=20_000, tolerance=0.2))
        if data_within_limits:
            pass_fig_name = PASS_PATH + 'AS-87_Freq_Res_PURE_TW_PASS.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                  title='AS-87: Frequency Response PURE - Tweeter Channel')
        else:
            fail_fig_name = FAIL_PATH + 'AS-87_Freq_Res_PURE_TW_FAIL.png'
            helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                  title='AS-87: Frequency Response PURE - Tweeter Channel')

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])

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
        measured_data = helpers.get_freq_res_xlr(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])

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
