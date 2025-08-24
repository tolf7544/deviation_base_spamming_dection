import random

import numpy as np
from numpy.random import Generator, PCG64

from python.delay_correlation_analysis import DelayCorrelationAnalysis
from python.metadata import DatasetMetadata
from python.util import load_numpy_array, quicksort



def display_delay_score(delay: np.ndarray, score: np.int64):
    print("[ delay score ]")
    for i in range(delay.__len__()):
        print("\tdelay: {}".format(delay[i]))

    print("\tscore {}".format(score))




if __name__ == '__main__':
    # analysis_test_1 = DelayCorrelationAnalysis(3, 100000, 1000, "delay_선형관계성")
    # analysis_test_1.generate_sample()
    group_size: int = 3
    group_count = 10
    max_deviation: int = 1000
    name: str = "analysis"

    analysis_test = DelayCorrelationAnalysis()
    analysis_test.set_metadata(3, 10000, 1000, "delay_선형관계성")
    print(analysis_test())

    # analysis_test_1 = DelayCorrelationAnalysis(3, 10000, 1000 * i, "delay_선형관계성")

    # for i in range(1, 3):
        # analysis_test = DelayCorrelationAnalysis(3, 10000, 1000 * i, "delay_선형관계성")
        # analysis_test.generate_sample()
        # analysis_test.analysis()
        # analysis_test.show_spread()
