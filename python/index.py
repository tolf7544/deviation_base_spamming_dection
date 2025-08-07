import random

import numpy as np
from numpy.random import Generator, PCG64

from python.delay_correlation_analysis import DelayCorrelationAnalysis
from python.util import load_numpy_array, quicksort



def display_delay_score(delay: np.ndarray, score: np.int64):
    print("[ delay score ]")
    for i in range(delay.__len__()):
        print("\tdelay: {}".format(delay[i]))

    print("\tscore {}".format(score))







if __name__ == '__main__':
    # analysis_test_1 = DelayCorrelationAnalysis(3, 100000, 1000, "delay_선형관계성")
    # analysis_test_1.generate_sample()
    # analysis_test_1.analysis()
    for i in range(1, 6):
        analysis_test = DelayCorrelationAnalysis(3, 1000000, 1000 * i, "delay_선형관계성")
        analysis_test.generate_sample()
        analysis_test.analysis()

