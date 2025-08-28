import codecs
import copy
import json
from tkinter.messagebox import RETRY

import numpy as np
from numpy.distutils.mingw32ccompiler import rc_name
from scipy.stats import boxcox, shapiro

from python.util import save_json_file
from python.variance_ratio_analysis import VarianceRatioAnalysis
limit = 0.1

def count_element(array: np.ndarray, dictionary: dict):
    for i in range(array.__len__()):
        key = np.round(array[i], 2)
        if dictionary.get(key) is None:
            dictionary[key] = 0
        dictionary[key] += 1


def __find_mean(lmbda_list, count_dict, size):
    mean = 0
    # lmbda의 빈도 수를 측정
    count_element(lmbda_list, count_dict)
    for key, value in list(count_dict.items()):
        mean += key * value
    mean /= size
    return mean


def get_mean_lmbda_analysis(vra, lmbda_list: np.ndarray, size):
    lmbda_dict: dict[float, int] = {}
    mean_lmbda = __find_mean(lmbda_list, lmbda_dict, size)
    sample, interval = vra.transformed_data()
    sample:np.ndarray = boxcox(sample, lmbda=mean_lmbda)
    for i in range(sample.__len__()):
        if sample[i] == -np.inf:
            sample[i] = 0

    sample = vra.min_max_normalization(sample)
    shapiro_result = shapiro(sample)
    return mean_lmbda, shapiro_result


def display_single_analysis(cases, shapiro_result, mean_lmbda, loop_count):
    error_list = np.empty(cases.__len__())
    error_dict = {}
    for i in range(cases.__len__()):
        error = cases[i][0] - shapiro_result[1]
        best_lmbda = np.round(cases[i][1], 2)
        lmbda_diff = np.round(cases[i][1] - mean_lmbda, 2)
        error_list[i] = error

        best_pvalue = np.round(cases[i][0], 2)
        mean_pvalue = np.round(shapiro_result[1], 2)
        pvalue_diff = np.round(error, 2)
        print("group_count {}".format(30 + i * 10), " * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("\tbest-lmbda {} mean-lmbda {} > lmbda_diff {}".format(best_lmbda, mean_lmbda, lmbda_diff))
        print("\tbest-pvalue {} mean-pvalue {} > pvalue-diff {}".format(best_pvalue, mean_pvalue, pvalue_diff))
        print("\n")
    error_mean = __find_mean(np.abs(error_list), error_dict, loop_count)
    print("total diff mean {}".format(error_mean))


def display_multi_analysis(checkpoint: dict):
    checkpoint_list = list(checkpoint.items())
    length = 0
    for i in range(checkpoint.__len__()):
        group_count, (cases, past_cases_analysis) = checkpoint_list[i]
        mean_lmbda, shapiro_result = past_cases_analysis
        if i == 0:
            length = group_count
        elif i+1 != checkpoint.__len__():
            length = group_count - checkpoint_list[i - 1][0]

        mean_cases_lmbda_error = np.abs(cases[:, 1] - mean_lmbda).sum() / length

        mean_cases_pvalue_error = np.abs(cases[:, 0] -shapiro_result[1]).sum() / length
        print("group_count {}".format(group_count), " * * * * * * * * * * * * * * * * * * * * * * * * *")
        print("\tmean-lmbda {} mean_error {}".format(mean_lmbda, mean_cases_lmbda_error))
        print("\tmean-pvalue {} mean_error {}".format(shapiro_result[1], mean_cases_pvalue_error))
        print("\n")


def save_single_analysis(vra, mean_lmbda, mean_pvalue, cases):
    save_object = {
        "range": "30-100",
        "limit": limit,
        "mean": {
            "lmbda": mean_lmbda,
            "pvalue": mean_pvalue,
        },
        "metadata": ["pvalue", "lmbda", "group_count"],
        "data": cases.tolist()
    }
    json_str = json.dumps(save_object, ensure_ascii=False)

    with open("{}/{}.json".format(vra.base_path,"total"), mode="w", encoding="utf-8") as f:
        f.write(json_str)


def save_multi_analysis(vra, checkpoint: dict):
    checkpoint_list = list(checkpoint.items())
    save_object = {
        "limit": limit,
        "mean_checkpoint": [],
        "cases_metadata": ["pvalue", "lmbda", "group_count"],
        "data_checkpoint": []
    }

    for i in range(checkpoint.__len__()):
        group_count, (cases, past_cases_analysis) = checkpoint_list[i]
        mean_lmbda, shapiro_result = past_cases_analysis
        if i == 0:
            length = group_count
        elif i+1 != checkpoint.__len__():
            length = group_count - checkpoint_list[i - 1][0]

        save_object["mean_checkpoint"].append({
            "group_count": group_count,
            "range": length,
            "lmbda": mean_lmbda,
            "pvalue": shapiro_result[1],
        })
        save_object["data_checkpoint"].append(cases.tolist())

    json_str = json.dumps(save_object, ensure_ascii=False)
    with open("{}/{}.json".format(vra.base_path,"total"), mode="w", encoding="utf-8") as f:
        f.write(json_str)

def find_multi_standard_lmbda(vra, cases, split_idx, past_cases_analysis, checkpoint, group_count):

    mean_lmbda, shapiro_result = get_mean_lmbda_analysis(vra, cases[:split_idx+1, 1], split_idx+1)  # shapiro_result: tuple(statistics, p-value)

    is_split = False
    if past_cases_analysis.__len__() == 0:
        past_cases_analysis = [mean_lmbda, shapiro_result]

    if shapiro_result[1] < limit:
        checkpoint[group_count] = [copy.deepcopy(cases[:split_idx+1]) , past_cases_analysis]
        cases = cases[split_idx:]
        # print(checkpoint)

        is_split = True
    else:
        past_cases_analysis = [mean_lmbda, shapiro_result]

    return cases, past_cases_analysis, is_split


def find_single_standard_lmbda(vra, cases, size):
    mean_lmbda, shapiro_result = get_mean_lmbda_analysis(vra, cases[:, 1], size)  # _result: tuple(statistics, p-value)
    # print("mean_lmbda {} pvalue {}".format(mean_lmbda, shapiro_result[1]))
    return mean_lmbda, shapiro_result


def analysis(vra, cases, idx, group_size, group_count, max_deviation, name):
    vra.set_metadata(group_size, group_count, max_deviation, name)
    vra.generate_sample()
    result, lmbda = vra.find_best_lmbda()

    cases[idx][0] = result[1]
    cases[idx][1] = lmbda
    cases[idx][2] = group_count

def find_standard_lmbda(is_single: bool = True):
    loop_count = (8 + 90) * 10
    group_size: int = 3
    max_deviation: int = 1000
    name: str = "boxcox standard lmbda analysis"

    cases = np.empty((loop_count, 3))
    checkpoint = {}
    vra = VarianceRatioAnalysis()
    idx = 0
    past_cases_analysis = []
    for i in range(loop_count):
        group_count = 30 + 1 * (i)
        analysis(vra, cases, idx, group_size, group_count, max_deviation, name)


        if is_single == False:
            cases, past_cases_analysis, is_split = find_multi_standard_lmbda(vra, cases, idx, past_cases_analysis,
                                                                             checkpoint, group_count)

            if group_count == 30 + (loop_count-1)*10:
                checkpoint[group_count] = [cases, past_cases_analysis]
            if is_split == True:
                idx = 0
                # cases에 이미 하나의 원소가 존재. 0으로 유지하여 다음 반복문 때 2번째 인덱스를 참조하도록 유도
        idx += 1

    if is_single == True:
        mean_lmbda, shapiro_result = find_single_standard_lmbda(vra, cases, idx) # idx는 반복문에서 마지막 +1로 인해 size와 동일한 크기를 가짐
        display_single_analysis(cases, shapiro_result, mean_lmbda, loop_count)
        save_single_analysis(vra, mean_lmbda, shapiro_result[1], cases)
    else:
        display_multi_analysis(checkpoint)
        save_multi_analysis(vra, checkpoint)


def display_graph():
    loop_count = (8 + 90)
    group_size: int = 3
    max_deviation: int = 1000
    name: str = "boxcox lmbda graph analysis"

    cases = np.empty((loop_count, 3))
    vra = VarianceRatioAnalysis()
    idx = 0

    for i in range(loop_count):
        group_count = 30 + 10 * (i)
        analysis(vra, cases, idx, group_size, group_count, max_deviation, name)
