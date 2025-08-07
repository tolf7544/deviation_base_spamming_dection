import codecs
import json
import os.path
from typing import Union, Optional

import numpy as np


def save_json_file(path, file_name, str):
    if os.path.exists(path) == False:
        os.mkdir(path)

    with open("{}/{}.json".format(path, file_name), encoding="utf-8", mode="w") as f:
        f.write(str)

def load_numpy_array(file_path): # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    obj_text = codecs.open(file_path, 'r', encoding='utf-8').read()
    b_new = json.loads(obj_text)
    a_new = np.array(b_new)

    return a_new



def partition(_array, is_array_element, comparing_index, low, high):
    if is_array_element == True:
        pivot = _array[high][comparing_index]
    else:
        pivot = _array[high]
    i = low - 1

    for j in range(low,high):
        if is_array_element == True:
            comparing_element = _array[j][comparing_index]
        else:
            comparing_element = _array[j]
        if comparing_element <= pivot:
            i += 1
            _array[[i, j]] = _array[[j, i]]

    _array[[i+1, high]] = _array[[high, i+1]]
    return i+1

def quicksort(_array: np.ndarray, is_array_element: bool = False, comparing_index: int = None, low: int=0, high: int=None) -> Union[Optional[list], np.ndarray]:
    if high == None:
        high = _array.__len__() - 1

    if low < high:
        pivot_index = partition(_array, is_array_element, comparing_index, low, high)
        quicksort(_array, is_array_element, comparing_index, low, pivot_index-1)
        quicksort(_array, is_array_element, comparing_index, pivot_index+1, high)

    return _array

