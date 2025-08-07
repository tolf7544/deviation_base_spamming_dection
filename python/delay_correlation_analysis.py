import codecs
import json
import os
from datetime import datetime
from math import floor

import numpy
import numpy as np
import pytz
from numpy.distutils.mingw32ccompiler import rc_name

from python.data.timestamp import generate_timestamp
from python.metadata import DatasetMetadata
from python.model.spam import delay_score
from python.util import save_json_file, load_numpy_array, quicksort
import matplotlib.pyplot as plt
from scipy.stats import t


class DelayCorrelationAnalysis(DatasetMetadata):
    def __init__(self, group_size: int = 3, group_count= 10,max_deviation: int = 1000, name: str = "analysis"):
        super().__init__(
            group_size=group_size,
            group_count=group_count,
            dtype=np.float64,
            max_deviation=max_deviation,
            name="G_{}_{}_d_{}_{}".format(group_size, group_count,max_deviation,  name),
            base_path="./data/dataset",
            description="score 범위 하위 25%, 상위 25% 집단만 분석"
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
        sample = np.empty((self.group_count, group_row_size), dtype=self.dtype)  # 0번째는 metadata 행

        for i in range(timestamps.__len__() // 3):
            _i = i * self.group_size  # group_size가 적용된 index / 두 index 사이에는 group_size만큼의 간격이 존재한다. (0,2) , (3, 6) , (7, 9)...
            timestamp_group = timestamps[_i:_i + self.group_size]
            result = delay_score(timestamp_group, self.dtype)
            sample[i] = np.concatenate(result)

        metadata = json.dumps(
            {
                "metadata": {
                    "time_zone": self.seoul_tz.__str__(),
                    "time_now": self.seoul_time.__str__(),
                    "group_count": self.group_count,
                    "group_size": self.group_size,
                    "data_type": self.dtype.__name__.__str__(),
                    "score_location": "last element",
                    "description": self.description
                }
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

    def load_save_dataset(self):
        return load_numpy_array(f"{self.dataset_folder_path}/dataset.json")

    def show_total_sample(self):
        sample = self.load_save_dataset()

        interval = 5
        y = np.zeros((100 // interval,), dtype=np.int64)
        x = np.arange(interval, 100 + interval, interval)

        for i in range(sample.__len__()):
            j = floor(sample[i][2] * 100) // interval
            if j > y.__len__() - 1:
                continue
            y[j] += 1

        plt.bar(x, y, width=1)
        plt.show()

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

    def analysis(self):
        sample = self.load_save_dataset()

        sample[:, 2] *= 100
        sample = sample.astype(np.int_)

        sample_upper_25 = []
        sample_lower_25 = []
        for i in range(sample.__len__()):
            if sample[i][2] >= 75:
                sample_upper_25.append(sample[i])
            if sample[i][2] <= 25:
                sample_lower_25.append(sample[i])

        sample_upper_25 = np.array(sample_upper_25)
        sample_lower_25 = np.array(sample_lower_25)

        upper_25 = self.corr_analysis(sample_upper_25)
        lower_25 = self.corr_analysis(sample_lower_25)
        total = self.corr_analysis(sample)
        print("total corr {} p-value {}".format(*total))
        save_json_file(self.dataset_folder_path, "result", "{"+f"\"corr\": {total[0]}, \"p-value\": {total[1]}"+"}")

    def corr_analysis(self, sample):
        x = sample[:, 0]  # 첫번째 딜레이
        y = sample[:, 1]  # 두번째 딜레이

        # # min-max 정규화
        # x_norm = self.min_max_normalization(x)
        # y_norm = self.min_max_normalization(y)

        # 공분산
        cov = self.cov(x, y)  # np.cov(x_norm, y_norm)[0,1]

        # 표준 편차
        x_sd = np.std(x, ddof=1)  # np.sqrt( np.sum((x_norm - x_norm.mean())**2)/x_norm.__len__() )
        y_sd = np.std(y, ddof=1)  # np.sqrt( np.sum((y_norm - y_norm.mean())**2)/y_norm.__len__() )

        # 피어슨 상관계수
        corr = cov / (x_sd * y_sd)

        # t-score
        t_score = corr * np.sqrt(sample.__len__() - 2) / np.sqrt(1 - corr ** 2)
        df = sample.__len__() - 1
        p_value = numpy.float64(t.sf(np.abs(t_score), df) * 2)

        return (corr, p_value)
