from typing import Any

import numpy as np



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
