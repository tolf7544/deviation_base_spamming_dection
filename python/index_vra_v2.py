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
from python.variance_ratio_analysis_v2 import SpamDetectorVarianceRatio

#d
#
#
# 이론적인 증명 & 학습 목적으로는 최적 람다 탐색 -> boxcox 변환 -> 샤피로 윌크 검정 을 기준으로 확인하는 휴리스틱이 존재하지만
# spicy의 boxcox에서 MLE를 통한 lmbda를 활용하는 것이 실무적으로 유용하다 판단.
#
# d

if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    group_size: int = 3
    group_count = 100
    max_deviation: int = 1000
    name: str = "spam detect by using variance ratio"

    vra = SpamDetectorVarianceRatio("data/dataset/G_3_100_d_1000_spam detect by using variance ratio/metadata.json")
    vra.set_metadata(group_size, group_count, max_deviation, name)
    vra.analysis()

    # for i in range(8):
    #     group_count = 30 + 10*(i)
    #     vra = SpamDetectorVarianceRatio()
    #     vra.set_metadata(group_size, group_count, max_deviation, name)
    #     vra.generate_sample()
    #     vra.analysis()



    # def differences(x_arr:list):
    #     result = np.empty(x_arr.__len__())
    #     for i in range(1, x_arr.__len__()):
    #         result[i-1] = x_arr[i] - x_arr[i-1]
    #
    #     return result
    #
    # def calculate_sequence_near_ratio(x_arr: list):
    #     result = np.empty(x_arr.__len__()-1)
    #     for i in range(x_arr.__len__()-1):
    #         if x_arr[i] == 0 or x_arr[i+1] == 0:
    #             continue
    #         result[i] = x_arr[i] / x_arr[i+1]
    #
    #     return result
    # with open("E:\Project\spam\deviation_base_spamming_dection\python\data\dataset\\vr_boxcox_lambda_analysis_v2\\total.json", encoding="utf-8", mode="r") as f:
    #     vra = VarianceRatioAnalysis()
    #     metadata = json.loads(f.read())
    #     mean_checkpoint = metadata["mean_checkpoint"]
    #     group_count_list = []
    #     lmbda_list = []
    #
    #     for i in range(mean_checkpoint.__len__()):
    #         if mean_checkpoint[i]["lmbda"] not in lmbda_list:
    #             lmbda_list.append(mean_checkpoint[i]["lmbda"])
    #             group_count_list.append(mean_checkpoint[i]["group_count"])
    #     np.set_printoptions(suppress=True)
    #     print(group_count_list)
    #     print(lmbda_list)
    #     plt.plot(vra.min_max_normalization(lmbda_list))
    #     plt.plot(vra.min_max_normalization(group_count_list))
    #     plt.show()
    #
