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
SHELVING_FILTERS = ['-12dB', '-6dB', '+6dB', '+12dB']
SHELVING_CUTOFF = ['400', '5000']
CH_DELAYS = ['0ms', '2.5ms', '5ms']
VOLUME = ['-60dB', '-12dB', '-6dB', '0dB', '+6dB', '+12dB']
CUSTOM_EQS = 6
SAMPLE_RATES = ['44_100Hz', '48_000Hz', '88_200Hz', '96_000Hz', '176_400Hz', '192_000Hz']
DUT_INPUTS = ['Analog', 'AESL', 'AESR']


# @pytest.mark.test_key('AS-87')
def set_dut_input(dut_input):
    print('\nPlease set the DUT input to ' + dut_input)
    proceed_meas = input('Confirm measurement [y/n]: ')
    return proceed_meas


@pytest.mark.parametrize('dut_input', ['Analog', 'AESL', 'AESR'])
class TestFrequencyResponsePURE:

    def test_frequency_response_pure_wf(self, dut_input):
        """
            AS-87 Frequency Response Pure
            :return:

        Parameters
        ----------
        CHANNEL
        """
        file_name = 'Ref_Freq_Res_PURE_0dB_' + dut_input + '_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=20, end_frequency=8_000, tolerance=0.4))
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
        file_name = 'Ref_Freq_Res_PURE_0dB_' + dut_input + '_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=100, end_frequency=20_000, tolerance=0.4))
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
        file_name = 'Ref_Freq_Res_PURE_0dB_' + dut_input + '_' + CHANNEL[2] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
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


@pytest.mark.parametrize('dut_input', ['Analog', 'AESL', 'AESR'])
class TestFrequencyResponseUNR:

    # @pytest.mark.test_key('AS-85')
    def test_frequency_response_unr_wf(self, dut_input):
        """
            AS-85 Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_UNR_0dB_' + dut_input + '_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=20, end_frequency=8_000, tolerance=0.4))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-85_Freq_Res_UNR_WF_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-85: Frequency Response UNR - Woofer Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-85_Freq_Res_UNR_WF_' + dut_input + 'FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-85: Frequency Response UNR - Woofer Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.test_key('AS-85')
    def test_frequency_response_unr_tw(self, dut_input):
        """
        AS-85 Frequency Response Pure
        :return:
        """
        file_name = 'Ref_Freq_Res_UNR_0dB_' + dut_input + '_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=100, end_frequency=20_000, tolerance=0.4))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-85_Freq_Res_UNR_TW_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-85: Frequency Response UNR - Tweeter Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-85_Freq_Res_UNR_TW_' + dut_input + '_FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-85: Frequency Response UNR - Tweeter Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    @pytest.mark.skipif(MODEL == 'S2V', reason='Selected model does not have a midrange channel')
    def test_frequency_response_unr_mr(self, dut_input):
        """
        AS-87 Frequency Response Pure
        :return:
        """
        file_name = 'Ref_Freq_Res_UNR_' + CHANNEL[2] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[2])
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=200, end_frequency=4_000, tolerance=0.1))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-85_Freq_Res_UNR_MR_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-85: Frequency Response UNR - Tweeter Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-85_Freq_Res_UNR_MR_' + dut_input + '_FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-85: Frequency Response UNR - Tweeter Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


@pytest.mark.parametrize('dut_input, volume',
                         [('Analog', VOLUME[0]), ('AESL', VOLUME[0]), ('AESR', VOLUME[0]),
                          ('Analog', VOLUME[1]), ('AESL', VOLUME[1]), ('AESR', VOLUME[1]),
                          ('Analog', VOLUME[2]), ('AESL', VOLUME[2]), ('AESR', VOLUME[2]),
                          ('Analog', VOLUME[3]), ('AESL', VOLUME[3]), ('AESR', VOLUME[3]),
                          ('Analog', VOLUME[4]), ('AESL', VOLUME[4]), ('AESR', VOLUME[4]),
                          ('Analog', VOLUME[5]), ('AESL', VOLUME[5]), ('AESR', VOLUME[5])])
class TestVolumeControl:

    # @pytest.mark.test_key('AS-291')
    def test_volume_control_wf(self, dut_input, volume):
        """
            AS-291 Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + volume + '_' + dut_input + '_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input + ' @ ' + volume)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
            if volume == '-60dB':
                tol = 2.0
            else:
                tol = 0.4
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=20, end_frequency=2_000, tolerance=tol))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_WF_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Woofer Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_WF_' + dut_input + '_FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Woofer Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.test_key('AS-291')
    def test_volume_control_tw(self, dut_input, volume):
        """
            AS-291 Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + volume + '_' + dut_input + '_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input + ' @ ' + volume)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
            if volume == '-60dB':
                tol = 2.0
            else:
                tol = 0.4
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=3_000, end_frequency=20_000, tolerance=tol))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_TW_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Tweeter Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_TW_' + dut_input + '_FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Tweeter Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.test_key('AS-291')
    @pytest.mark.skipif(MODEL == 'S2V', reason='Selected model does not have a midrange channel')
    def test_volume_control_mr(self, dut_input, volume):
        """
            AS-291 Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + volume + '_' + dut_input + '_' + CHANNEL[2] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input + ' @ ' + volume)
        if proceed_meas == 'y':
            measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[2])
            if volume == '-60dB':
                tol = 2.0
            else:
                tol = 0.4
            data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                       start_frequency=200, end_frequency=4_000, tolerance=tol))
            if data_within_limits:
                pass_fig_name = PASS_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_MR_' + dut_input + '_PASS.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=pass_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Midrange Channel')
            else:
                fail_fig_name = FAIL_PATH + 'AS-291_Freq_Res_PURE_' + volume + '_MR_' + dut_input + '_FAIL.png'
                helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data, fig_path=fail_fig_name,
                                      title='AS-291: Frequency Response PURE @ ' + volume + ' - Midrange Channel')

            assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


@pytest.mark.parametrize('dut_input, ch_delay',
                         [(DUT_INPUTS[0], CH_DELAYS[0]), (DUT_INPUTS[1], CH_DELAYS[0]), (DUT_INPUTS[2], CH_DELAYS[0]),
                          (DUT_INPUTS[0], CH_DELAYS[1]), (DUT_INPUTS[1], CH_DELAYS[1]), (DUT_INPUTS[2], CH_DELAYS[1]),
                          (DUT_INPUTS[0], CH_DELAYS[2]), (DUT_INPUTS[1], CH_DELAYS[2]), (DUT_INPUTS[2], CH_DELAYS[2])])
class TestDelay:

    # @pytest.mark.test_key('AS-88')
    def test_delay_wf(self, dut_input, ch_delay):
        """
        AS-88 Woofer Channel Delay Test
        :return:
        """
        file_name = 'Ref_Delay_PURE_' + ch_delay + '_' + dut_input + '_' + CHANNEL[0] + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        proceed_meas = set_dut_input(dut_input + ' with ' + ch_delay + ' delay')
        if proceed_meas == 'y':
            measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
            meas_ref_ratio = measured_data['channel_delay'][0] / reference_data[0]
            deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
            tolerance = 10  # Tolerance in percentage

            woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                            'Measured Delay': ' ' + str(measured_data['channel_delay'][0]) + ' s',
                            'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

            if deviation <= tolerance:
                pass_txt_name = PASS_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[0] + '_PASS.txt'
                with open(pass_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))
            else:
                fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[0] + '_FAIL.txt'
                with open(fail_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))

            assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    # @pytest.mark.test_key('AS-88')
    def test_delay_tw(self, dut_input, ch_delay):
        """
        AS-88 Tweeter Channel Delay Test
        :return:
        """
        file_name = 'Ref_Delay_PURE_' + ch_delay + '_' + dut_input + '_' + CHANNEL[1] + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        proceed_meas = set_dut_input(dut_input + ' with ' + ch_delay + ' delay')
        if proceed_meas == 'y':
            measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
            meas_ref_ratio = measured_data['channel_delay'][1] / reference_data[0]
            deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
            tolerance = 10  # Tolerance in percentage

            woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                            'Measured Delay': ' ' + str(measured_data['channel_delay'][1]) + ' s',
                            'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

            if deviation <= tolerance:
                pass_txt_name = PASS_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[1] + '_PASS.txt'
                with open(pass_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))
            else:
                fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[1] + '_FAIL.txt'
                with open(fail_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))

            assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'

    @pytest.mark.skipif(MODEL == 'S2V', reason='Selected model does not have a midrange channel')
    # @pytest.mark.test_key('AS-88')
    def test_delay_mr(self, dut_input, ch_delay):
        """
        AS-88 Midrange Channel Delay Test
        :return:
        """
        file_name = 'Ref_Delay_PURE_' + ch_delay + '_' + dut_input + '_' + CHANNEL[2] + '_s.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name))[0].astype(float)
        proceed_meas = set_dut_input(dut_input + ' with ' + ch_delay + ' delay')
        if proceed_meas == 'y':
            measured_data = helpers.get_delay(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[2])
            meas_ref_ratio = measured_data['channel_delay'][2] / reference_data[0]
            deviation = np.abs(1 - meas_ref_ratio) * 100  # Deviation error in percentage
            tolerance = 10  # Tolerance in percentage

            woofer_delay = {'Reference Delay': ' ' + str(reference_data[0]) + ' s',
                            'Measured Delay': ' ' + str(measured_data['channel_delay'][2]) + ' s',
                            'Tolerance': ' ' + str(tolerance) + ' %', 'Deviation': ' ' + str(deviation) + ' %'}

            if deviation <= tolerance:
                pass_txt_name = PASS_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[2] + '_PASS.txt'
                with open(pass_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))
            else:
                fail_txt_name = FAIL_PATH + 'AS-88_Delay_' + ch_delay + '_' + dut_input + '_' + CHANNEL[2] + '_FAIL.txt'
                with open(fail_txt_name, 'w') as f:
                    for key, value in woofer_delay.items():
                        f.write('%s:%s\n' % (key, value))

            assert deviation <= tolerance, 'Measured delay is not within the specified tolerance'


@pytest.mark.parametrize('dut_input, sample_rate',
                         [(DUT_INPUTS[1], SAMPLE_RATES[0]), (DUT_INPUTS[2], SAMPLE_RATES[0]),
                          (DUT_INPUTS[1], SAMPLE_RATES[1]), (DUT_INPUTS[2], SAMPLE_RATES[1]),
                          (DUT_INPUTS[1], SAMPLE_RATES[2]), (DUT_INPUTS[2], SAMPLE_RATES[2]),
                          (DUT_INPUTS[1], SAMPLE_RATES[3]), (DUT_INPUTS[2], SAMPLE_RATES[3]),
                          (DUT_INPUTS[1], SAMPLE_RATES[4]), (DUT_INPUTS[2], SAMPLE_RATES[4]),
                          (DUT_INPUTS[1], SAMPLE_RATES[5]), (DUT_INPUTS[2], SAMPLE_RATES[5])])
class TestAESSampleRate:

    # @pytest.mark.test_key('AS-292')
    def test_sample_rate_wf(self, dut_input, sample_rate):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        input_config = set_dut_input(dut_input)
        if input_config == 'y':
            print('Please set the sample rate in the output configuration of the AP project to ' + sample_rate
                  + ' and save the file')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
                data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                           start_frequency=20, end_frequency=8_000, tolerance=0.4))
                if data_within_limits:
                    pass_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_WF_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=pass_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Woofer Channel')
                else:
                    fail_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_WF_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=fail_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Woofer Channel')

                assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.test_key('AS-292')
    def test_sample_rate_tw(self, dut_input, sample_rate):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        input_config = set_dut_input(dut_input)
        if input_config == 'y':
            print('Please set the sample rate in the output configuration of the AP project to ' + sample_rate
                  + ' and save the file')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
                data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                           start_frequency=100, end_frequency=20_000, tolerance=0.4))
                if data_within_limits:
                    pass_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_TW_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=pass_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Tweeter Channel')
                else:
                    fail_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_TW_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=fail_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Tweeter Channel')

                assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    @pytest.mark.skipif(MODEL == 'S2V', reason='Selected model does not have a midrange channel')
    # @pytest.mark.test_key('AS-292')
    def test_sample_rate_mr(self, dut_input, sample_rate):
        """
            AS-XX Frequency Response Pure
            :return:
        """
        file_name = 'Ref_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_' + CHANNEL[2] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        input_config = set_dut_input(dut_input)
        if input_config == 'y':
            print('Please set the sample rate in the output configuration of the AP project to ' + sample_rate
                  + ' and save the file')
            proceed_meas = input('Confirm measurement [y/n]: ')
            if proceed_meas == 'y':
                measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[2])
                data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                           start_frequency=300, end_frequency=6_000, tolerance=0.4))
                if data_within_limits:
                    pass_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_TW_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=pass_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Midrange Channel')
                else:
                    fail_fig_name = PASS_PATH + 'AS-292_Freq_Res_PURE_' + sample_rate + '_' + dut_input + '_TW_PASS.png'
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=fail_fig_name,
                                          title='AS-292: Frequency Response ' + dut_input + ' Input @ ' + sample_rate +
                                                ' - Midrange Channel')

                assert data_within_limits, 'Measured frequency response is not within the specified tolerance'


@pytest.mark.parametrize('dut_input, filter_gain',
                         [(DUT_INPUTS[0], SHELVING_FILTERS[0]), (DUT_INPUTS[1], SHELVING_FILTERS[0]),
                          (DUT_INPUTS[2], SHELVING_FILTERS[0]), (DUT_INPUTS[0], SHELVING_FILTERS[1]),
                          (DUT_INPUTS[1], SHELVING_FILTERS[1]), (DUT_INPUTS[2], SHELVING_FILTERS[1]),
                          (DUT_INPUTS[0], SHELVING_FILTERS[2]), (DUT_INPUTS[1], SHELVING_FILTERS[2]),
                          (DUT_INPUTS[2], SHELVING_FILTERS[2]), (DUT_INPUTS[0], SHELVING_FILTERS[3]),
                          (DUT_INPUTS[1], SHELVING_FILTERS[3]), (DUT_INPUTS[2], SHELVING_FILTERS[3])])
class TestShelvingFilters:

    # @pytest.mark.test_key('AS-293')
    def test_lo_shelf_wf(self, dut_input, filter_gain):
        """
            AS-293
            :return:
        """
        file_name = 'Ref_Freq_Res_USER_1_' + dut_input + '_' + filter_gain + '_' + CHANNEL[0] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input + ' and select Slot C')
        if proceed_meas == 'y':
            print('Please set the DUT Lo-Shelf cutoff frequency to ' + SHELVING_CUTOFF[0] + ' Hz and set the gain to '
                  + filter_gain)
            print('Please set the DUT Hi-Shelf cutoff frequency to ' + SHELVING_CUTOFF[1] + ' Hz and set the gain to '
                  + filter_gain)
            confirm_meas = input('Confirm measurement [y/n]: ')
            if confirm_meas == 'y':
                measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[0])
                data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                           start_frequency=20, end_frequency=8_000, tolerance=0.4))
                if data_within_limits:
                    pass_fig_name = (PASS_PATH + 'AS-293_Freq_Res_Lo_Shelf_' + dut_input + '_' + filter_gain
                                     + '_WF_PASS.png')
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=pass_fig_name, title='AS-293: Frequency Response Lo-Shelf '
                                                                        + dut_input + ' ' + filter_gain
                                                                        + ' - Woofer Channel')
                else:
                    fail_fig_name = (FAIL_PATH + 'AS-293_Freq_Res_Lo_Shelf_' + dut_input + '_' + filter_gain
                                     + '_WF_FAIL.png')
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=fail_fig_name, title='AS-293: Frequency Response Lo-Shelf '
                                                                        + dut_input + ' ' + filter_gain
                                                                        + ' - Woofer Channel')

                assert data_within_limits, 'Measured frequency response is not within the specified tolerance'

    # @pytest.mark.test_key('AS-293')
    def test_lo_shelf_tw(self, dut_input, filter_gain):
        """
            AS-293
            :return:
        """
        file_name = 'Ref_Freq_Res_USER_1_' + dut_input + '_' + filter_gain + '_' + CHANNEL[1] + '_dBFS.csv'
        reference_data = (helpers.load_csv(FILE_PATH, file_name)).astype(float)
        proceed_meas = set_dut_input(dut_input + ' and select Slot C')
        if proceed_meas == 'y':
            print('Please set the DUT Lo-Shelf cutoff frequency to ' + SHELVING_CUTOFF[0] + ' Hz and set the gain to '
                  + filter_gain)
            print('Please set the DUT Hi-Shelf cutoff frequency to ' + SHELVING_CUTOFF[1] + ' Hz and set the gain to '
                  + filter_gain)
            confirm_meas = input('Confirm measurement [y/n]: ')
            if confirm_meas == 'y':
                measured_data = helpers.get_freq_res(project=AP_SEQ_FREQUENCY_RESPONSE_XLR, channel=CH_IDX[1])
                data_within_limits = (helpers.check_limits(data=measured_data['rms_level'], ref_data=reference_data,
                                                           start_frequency=100, end_frequency=20_000, tolerance=0.4))
                if data_within_limits:
                    pass_fig_name = (PASS_PATH + 'AS-293_Freq_Res_Hi_Shelf_' + dut_input + '_' + filter_gain
                                     + '_TW_PASS.png')
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=pass_fig_name, title='AS-293: Frequency Response Hi-Shelf '
                                                                        + dut_input + ' ' + filter_gain
                                                                        + ' - Tweeter Channel')
                else:
                    fail_fig_name = (FAIL_PATH + 'AS-293_Freq_Res_Hi_Shelf_' + dut_input + '_' + filter_gain
                                     + '_TW_FAIL.png')
                    helpers.save_freq_res(data=measured_data['rms_level'], ref_data=reference_data,
                                          fig_path=fail_fig_name, title='AS-293: Frequency Response Hi-Shelf '
                                                                        + dut_input + ' ' + filter_gain
                                                                        + ' - Tweeter Channel')

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
