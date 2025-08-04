import codecs
import os

from python.data.timestamp import generate_timestamp
from python.metadata import GROUP_SIZE, USE_DTYPE, GROUP_COUNT, DATASET_BASE_PATH, DATASET_NAME
from python.model.spam import delay_score

import json
from datetime import datetime

import numpy as np
import pytz

from python.util import save_json_file, load_numpy_array

seoul_tz = pytz.timezone('Asia/Seoul')
seoul_time = datetime.now(seoul_tz)


def display_delay_score(delay: np.ndarray, score: np.int64):
    print("[ delay score ]")
    for i in range(delay.__len__()):
        print("\tdelay: {}".format(delay[i]))

    print("\tscore {}".format(score))


def analysis_test_1():
    sample = generate_timestamp(size=GROUP_SIZE * GROUP_COUNT, start_ms=1000, max_deviation=1000)

    group_row_size = 2 * GROUP_SIZE - 3
    # delay_group_count = group_size-1;
    # score_group_count = delay_group_count -1;
    # total_count = delay_group_count + score_group_count
    # total_count = (group_size-1) + {(group_size-1)-1}
    # total_count = group_size*2 - 3
    group = np.empty((GROUP_COUNT, group_row_size), dtype=USE_DTYPE)  # 0번째는 metadata 행

    for i in range(0, sample.__len__(), GROUP_SIZE):
        timestamp_group = sample[i:i + GROUP_SIZE]
        result = delay_score(timestamp_group)
        # display_delay_score(delays, score)
        group[i // 3] = np.concatenate(result)

    folder_count = os.listdir(DATASET_BASE_PATH).__len__()

    metadata = json.dumps(
        {
            "metadata": {
                "time_zone": seoul_tz.__str__(),
                "time_now": seoul_time.__str__(),
                "group_count": GROUP_COUNT,
                "group_size": GROUP_SIZE,
                "data_type": USE_DTYPE.__name__.__str__(),
                "score_location": "last element",
                "description": "score 범위 80%~100% 사이인 집단만 분석"
            }
        },
        ensure_ascii=False
    )

    path = "{}/{}".format(DATASET_BASE_PATH, DATASET_NAME)
    save_json_file(path=path,
                   file_name="metadata",
                   str=metadata)
    # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    json.dump(group.tolist(), codecs.open(f"{path}/dataset.json", 'w', encoding='utf-8'),
              separators=(',', ':'),
              sort_keys=True,
              indent=4)


if __name__ == '__main__':
    analysis_test_1()
    np_arr = load_numpy_array(f"{DATASET_BASE_PATH}/{DATASET_NAME}/dataset.json")
    print(np_arr)