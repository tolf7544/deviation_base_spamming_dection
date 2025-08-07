import os
from datetime import datetime

import numpy as np
import pytz


class DatasetMetadata:
    def __init__(self, group_size: int = 5, group_count: int = 1, max_deviation: int = 1000,seed: int = 1234, dtype: np.dtype = np.float64,
                 name: str = None, base_path: str = "./data/dataset",
                 description: str = None):
        self.seed = seed
        self.group_size = group_size
        self.group_count = group_count
        self.max_deviation =max_deviation
        self.dtype = dtype

        self.name = name  # "spam_dector_v2_1_delay_correlation_check_1"
        self.base_path = base_path
        self.__set_data_folder_path()
        self.description = description

        self.seoul_tz = pytz.timezone('Asia/Seoul')
        self.seoul_time = datetime.now(self.seoul_tz)

    def __set_data_folder_path(self):
        default_dataset_folder_path = "{}/{}".format(self.base_path, self.name)
        save_folder_count = [path.find(default_dataset_folder_path) != -1 for path in os.listdir(self.base_path)].__len__()

        if os.path.exists(default_dataset_folder_path):
            self.dataset_folder_path = "{}_{}".format(default_dataset_folder_path, save_folder_count)
        else:
            self.dataset_folder_path = default_dataset_folder_path