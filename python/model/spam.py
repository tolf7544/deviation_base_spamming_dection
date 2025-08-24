from typing import Any

import numpy as np

from python.util import absolute_subtract


def delay_score(message_timestamp: np.ndarray, dtype: np.dtype):

    delay_count = message_timestamp.__len__() - 1
    score_count = delay_count - 1
    delays = np.empty(delay_count, dtype=dtype)
    scores = np.empty(score_count, dtype=dtype)

    for i in range(delay_count):

        delays[i] = message_timestamp[i + 1] - message_timestamp[i]

        if i != 0 and (i+1) % 2 == 0:
            scores[i // 2] = min(delays[i - 1], delays[i]) / max(delays[i - 1], delays[i])

    return [delays, scores]

def mean_variance_ratio(group: np.ndarray, dtype: np.dtype, epsilon: int = 1e-5):
    transformed: np.ndarray = np.log(group)

    mean = transformed.mean()
    deviation = np.abs(group - mean + epsilon)

    mad = 1 / deviation.__len__() * deviation.sum()
    group = deviation / mad # variance_distances 절대 편차 평균으로 정규화 ( 총합: 샘플점 갯수 )

    variance_ratio = np.empty(group.__len__()-1, dtype= dtype)
    for i in range(group.__len__()-1):
        variance_ratio[i] = min(group[i], group[i+1]) / max(group[i], group[i+1])
    return variance_ratio.mean()
