import codecs
import json
import os
from datetime import datetime
from math import floor
from random import sample
from typing import Union, AnyStr

import numpy
import numpy as np
import pytz

from python.data.timestamp import generate_timestamp
from python.metadata import DatasetMetadata
from python.model.spam import delay_score, mean_variance_ratio
from python.util import save_json_file, load_numpy_array, quicksort, standardization
import matplotlib.pyplot as plt
from scipy.stats import t, shapiro, boxcox, norm, anderson


class SpamDetectorVarianceRatio(DatasetMetadata):
    def __init__(self,path: Union[os.PathLike[str], str] = None):
        if path != None and os.path.exists(path):
            with open(path, mode="r", encoding="utf-8") as f:
                string = f.read()
                metadata = json.loads(string)["metadata"]
                super().__init__(**metadata)

    def set_metadata(self, group_size: int = 3, group_count= 10,max_deviation: int = 1000, name: str = "analysis"):
        super().__init__(
            group_size=group_size,
            group_count=group_count,
            dtype=np.float64,
            max_deviation=max_deviation,
            name="G_{}_{}_d_{}_{}".format(group_size, group_count,max_deviation,  name),
            base_path="./data/dataset",
            description="분산_비율_스팸_탐지_정의 v1"
        )


    def generate_sample(self):
        timestamps = generate_timestamp(seed=self.seed, size=self.group_size * self.group_count, start_ms=1000,
                                        interval=self.group_size,
                                        max_deviation=self.max_deviation, dtype=self.dtype)

        group_row_size = 2 * self.group_size - 3
        # delay_group_count = group_size-1;
        # score_group_count = delay_group_count -1;
        # total_count = delay_group_count + score_group_count
        # total_count = (group_size-1) + {(group_size-1)-1}
        # total_count = group_size*2 - 3
        sample = np.empty((self.group_count), dtype=self.dtype)  # 0번째는 metadata 행

        for i in range(timestamps.__len__() // self.group_size):
            _i = i * self.group_size  # group_size가 적용된 index / 두 index 사이에는 group_size만큼의 간격이 존재한다. (0,2) , (3, 6) , (7, 9)...
            timestamp_group = timestamps[_i:_i + self.group_size]
            result = mean_variance_ratio(timestamp_group, self.dtype)
            sample[i] = result

        metadata = json.dumps(
            {
                "metadata": self()
            },
            ensure_ascii=False
        )

        save_json_file(path=self.dataset_folder_path,
                       file_name="metadata",
                       str=metadata)
        # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
        np.set_printoptions(suppress=True)
        # sample = quicksort(sample, is_array_element=True, comparing_index=2)  # score 기준 정렬

        json.dump(sample.tolist(),
                  codecs.open(f"{self.dataset_folder_path}/dataset.json", 'w', encoding='utf-8'),
                  separators=(',', ':'),
                  sort_keys=True,
                  indent=4)

    def load_save_dataset(self)-> np.ndarray:
        return load_numpy_array(f"{self.dataset_folder_path}/dataset.json")

    def transformed_data(self, interval:float = 1):
        sample = self.load_save_dataset()
        sample = sample * 100
        return sample, interval


    def min_max_normalization(self, x) -> np.ndarray:
        x_max = np.max(x)
        x_min = np.min(x)
        x_norm = (x - x_min) / (x_max - x_min)
        return x_norm

    def analysis(self):
        sample, interval = self.transformed_data()
        sample, lmbda = boxcox(sample)
        if sample.__len__() > 50:
            test_result = anderson(sample)
            print(test_result)
            failed_list = test_result[1][test_result[1] <= test_result[0]]

            if failed_list.__len__() == 0:
                print("success")
            else:
                print("failed")
        else:
            test_result = shapiro(sample)
            print(test_result)
            print("sample size {} lambda {}".format(sample.__len__(), lmbda))





        self.show_sample(sample, interval)
        sample = standardization(sample)
        self.show_sample(sample, interval)

        _mean = sample.mean()
        _std = sample.std()
        alpha_list = [0.05, 0.1, 0.15]
        for alpha in alpha_list:
            critical_value = 1 - alpha
            boundary_value = norm.ppf(critical_value, _mean, _std)
            filtered_data = sample[sample >= boundary_value]

            print("boundary_value {}".format(boundary_value))
            filtered_data_len = filtered_data.__len__()
            _s_len = sample.__len__()
            _ratio = filtered_data_len / _s_len * 100
            print("| filtered data |")
            print("{}".format(np.array2string(filtered_data)))
            #https://stackoverflow.com/questions/60699836/how-to-use-norm-ppf
            print("\t[ {} / {} ] 총 {}% 필터링 됨.".format(filtered_data_len, _s_len, _ratio))
            print("\n")




    def show_sample(self, sample, interval): # https://jimmy-ai.tistory.com/74

        # plt.hist(sample, color='green', alpha=0.4, range=_range, label='data1')
        plt.hist(sample, color='red', alpha=0.5, label='data2', histtype = 'step')
        plt.show()
