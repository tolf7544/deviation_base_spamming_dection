import random

import numpy as np
from numpy.random import Generator, PCG64

from python.delay_correlation_analysis import DelayCorrelationAnalysis
from python.metadata import DatasetMetadata
from python.util import load_numpy_array, quicksort
from python.variance_ratio_analysis import VarianceRatioAnalysis

if __name__ == '__main__':
    group_size: int = 3
    group_count = 100000
    max_deviation: int = 1000
    name: str = "variance ratio analysis"
    vra = VarianceRatioAnalysis()
    vra.set_metadata(group_size, group_count, max_deviation, name)
    vra.generate_sample()
    vra.show_total_sample()

    # analysis_test_1 = DelayCorrelationAnalysis(3, 10000, 1000 * i, "delay_선형관계성")

    # for i in range(1, 3):
        # analysis_test = DelayCorrelationAnalysis(3, 10000, 1000 * i, "delay_선형관계성")
        # analysis_test.generate_sample()
        # analysis_test.analysis()
        # analysis_test.show_spread()
