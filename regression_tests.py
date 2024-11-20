import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import helpers

matplotlib.use('TkAgg')


@pytest.mark.xray('AS-87')
def test_frequency_response_pure():
    expected_output = f'DeviceName {{ {DEV} }}\n'

    assert Utility.get_canonical_name(DEV) == expected_output
