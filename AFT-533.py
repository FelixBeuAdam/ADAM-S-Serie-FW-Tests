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
AP_SEQ_FREQUENCY_RESPONSE_XLR = os.path.join(FILE_PATH, 'AP Sequences\\Frequency_Response_XLR.approjx')

APx = APx500_Application()
APx.OpenProject(AP_SEQ_FREQUENCY_RESPONSE_XLR)
APx.Visible = True

with open("S2V-TW.csv", 'r') as x:
    sample_data = list(csv.reader(x, delimiter=";"))

sample_data = np.array(sample_data[4:-5])
sample_data = (np.vstack(sample_data)[:, :-1]).astype(float)

plt.semilogx(sample_data[:, 0], sample_data[:, 1])
plt.grid()
plt.show()

