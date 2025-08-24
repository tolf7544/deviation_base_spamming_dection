import json
import os
from datetime import datetime
from typing import AnyStr

import numpy as np
import pytz


class DatasetMetadata:
    def __init__(self, group_size: int = 5, group_count: int = 1,
                 max_deviation: int = 1000, seed: int = 1234, dtype: np.dtype = np.float64,
                 name: str = None, base_path: str = "./data/dataset",
                 description: str = None, tz: str = None, saved_time: str = None):

        self.seed = seed
        self.group_size = group_size
        self.group_count = group_count
        self.max_deviation = max_deviation

        self.name = name
        self.base_path = base_path
        self.description = description
        self.__set_data_folder_path()
        self.__set_dtype_metadata(dtype)

        self.__set_time_metadata(tz, saved_time)

    def __set_dtype_metadata(self, data_type):
        if isinstance(data_type, str):
            self.dtype = getattr(np, data_type)
        else:
            self.dtype = data_type

    def __set_time_metadata(self, tz, saved_time):
        if tz != None:
            self.seoul_tz = pytz.timezone(tz)
        else:
            self.seoul_tz = pytz.timezone('Asia/Seoul')

        if saved_time != None:
            self.seoul_time = saved_time
        else:
            self.seoul_time = datetime.now(self.seoul_tz).__str__()

    def __set_data_folder_path(self):
        default_dataset_folder_path = "{}/{}".format(self.base_path, self.name)
        save_folder_count = [path.find(default_dataset_folder_path) != -1 for path in
                             os.listdir(self.base_path)].__len__()

        if os.path.exists(default_dataset_folder_path):
            self.dataset_folder_path = "{}_{}".format(default_dataset_folder_path, save_folder_count)
        else:
            self.dataset_folder_path = default_dataset_folder_path

    def __call__(self, *args, **kwargs):
        return {
            "seed": self.seed,
            "group_size": self.group_size,
            "group_count": self.group_count,
            "max_deviation": self.max_deviation,
            "dtype": self.dtype.__name__.__str__(),
            "name": self.name,
            "description": self.description,
            "base_path": self.base_path,
            "tz": self.seoul_tz.__str__(),
            "save_time": self.seoul_time
        }
