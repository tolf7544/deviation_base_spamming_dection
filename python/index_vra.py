import json
import random

import numpy as np
from matplotlib import pyplot as plt
from numpy.random import Generator, PCG64

from python.boxcox_lmbda_analysis import find_standard_lmbda
from python.delay_correlation_analysis import DelayCorrelationAnalysis
from python.metadata import DatasetMetadata
from python.util import load_numpy_array, quicksort
from python.variance_ratio_analysis import VarianceRatioAnalysis


if __name__ == '__main__':
    # np.set_printoptions(suppress=True)
    # group_size: int = 3
    # group_count = 100000
    #
    # max_deviation: int = 1000
    # name: str = "variance ratio analysis"
    # # vra = VarianceRatioAnalysis()
    # # vra.set_metadata(group_size, group_count, max_deviation, name)
    # # vra.generate_sample()
    # # vra.find_best_lmbda()
    #
    #
    # vra = VarianceRatioAnalysis()
    # vra.set_metadata(group_size, group_count, max_deviation, name)
    # vra.generate_sample()
    # vra.show_total_sample()
    #
    # for i in range(8):
    #     group_count = 30 + 10*(i)
    #     vra = VarianceRatioAnalysis()
    #     vra.set_metadata(group_size, group_count, max_deviation, name)
    #     vra.generate_sample()
    #     result = vra.find_best_lmbda()
    #     print(result)

    def differences(x_arr:list):
        result = np.empty(x_arr.__len__())
        for i in range(1, x_arr.__len__()):
            result[i-1] = x_arr[i] - x_arr[i-1]

        return result

    def calculate_sequence_near_ratio(x_arr: list):
        result = np.empty(x_arr.__len__()-1)
        for i in range(x_arr.__len__()-1):
            if x_arr[i] == 0 or x_arr[i+1] == 0:
                continue
            result[i] = x_arr[i] / x_arr[i+1]

        return result
    with open("E:\Project\spam\deviation_base_spamming_dection\python\data\dataset\\vr_boxcox_lambda_analysis_v4\\total.json", encoding="utf-8", mode="r") as f:
        vra = VarianceRatioAnalysis()
        metadata = json.loads(f.read())
        mean_checkpoint = metadata["mean_checkpoint"]
        group_count_list = []
        lmbda_list = []

        for i in range(mean_checkpoint.__len__()):
            if mean_checkpoint[i]["lmbda"] not in lmbda_list:
                lmbda_list.append(mean_checkpoint[i]["lmbda"])
                group_count_list.append(mean_checkpoint[i]["group_count"])
        np.set_printoptions(suppress=True)
        print(group_count_list)
        print(lmbda_list)
        plt.plot(vra.min_max_normalization(lmbda_list))
        plt.plot(vra.min_max_normalization(group_count_list))
        plt.show()

    # find_standard_lmbda(False)

# y = ax

# A 1
# B 5

# C