import codecs
import json
import os.path

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