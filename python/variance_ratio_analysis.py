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
from numpy.distutils.mingw32ccompiler import rc_name

from python.data.timestamp import generate_timestamp
from python.metadata import DatasetMetadata
from python.model.spam import delay_score, mean_variance_ratio
from python.util import save_json_file, load_numpy_array, quicksort
import matplotlib.pyplot as plt
from scipy.stats import t, shapiro, boxcox, stats


class VarianceRatioAnalysis(DatasetMetadata):
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
            description="분산_기반_스팸_탐지_정의 v3"
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
        sample = self.min_max_normalization(sample)
        sample = (sample * 100) // interval
        return sample, interval


    def find_best_lmbda(self):
        result = [0,0]
        lmbda = 0

        for i in range(1, 300):
            _lmbda = -1 + 0.01 * i
            sample, interval = self.transformed_data()
            sample = boxcox(sample, lmbda=_lmbda)

            sample = self.min_max_normalization(sample)
            _result = shapiro(sample)

            if result[1] < _result[1]:
                result = _result
                lmbda = _lmbda

        return result, lmbda

    def min_max_normalization(self, x) -> np.ndarray:
        x_max = np.max(x)
        x_min = np.min(x)
        x_norm = (x - x_min) / (x_max - x_min)
        return x_norm

    def cov(self, x: np.ndarray, y: np.ndarray):  # np.corrcoef(x,y)
        scalar = 0
        # 평균
        x_mean = x.mean()
        y_mean = y.mean()
        for i in range(x.__len__()):
            scalar += (x[i] - x_mean) * (y[i] - y_mean)

        return scalar / (x.__len__() - 1)  # 자유도 적용

    def show_total_sample(self):
        sample = self.load_save_dataset()
        sample = self.min_max_normalization(sample)

        shape = 100 + 1
        y = np.zeros((shape,), dtype=np.int64)
        x = np.arange(0, shape, 1)
        for i in range(sample.__len__()):
            j = int(sample[i]*100)
            y[j] += 1
        plt.bar(x, y, width=1)
        plt.show()


    def show_sample(self, sample, interval):
        # normalized_sample = self.min_max_normalization(sample)
        shape = 100 // interval + 1
        y = np.zeros((shape,), dtype=np.int64)
        x = np.arange(0, shape, 1)
        for i in range(sample.__len__()):
            j = int(sample[i])
            y[j] += 1
        plt.bar(x, y, width=1)
        plt.show()

    def show_spread(self):
        sample = self.load_save_dataset()
        sample[:, 2] *= 100
        x = sample[:,0]
        y = sample[:,1]
        sample_upper_25 = []
        sample_lower_25 = []



        plt.scatter(x, y, color='skyblue', alpha=0.7, s=0.5)
        plt.title('산포도')
        plt.xlabel('delay i')
        plt.ylabel('delay i+1')
        plt.grid(True)
        plt.show()
