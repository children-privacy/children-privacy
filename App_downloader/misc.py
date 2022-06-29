# misc.py

import datetime
import os

def get_date():
    date = datetime.datetime.now()
    return date.strftime("%d") + date.strftime("%b") + date.strftime("%Y")

def rename_folder_by_size(folder_path, n):
    new_name = folder_path + '_' + str(n)
    os.rename(folder_path, new_name)
    print('Rename the folder as ', new_name)

def get_n_files(folder_path):
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        return len(filenames)

def merge_dict3(dict1, dict2, dict3):
    res = {**dict1, **dict2, **dict3}
    return res

def convert_to_zero_one(items, pool):
    out = []
    for item in pool:
        if item in items:
            out.append(1)
        else:
            out.append(0)
    return out

def convert_to_zero_one_accumulate(self, items):
    out = []
    if len(items):
        out = [0] * len(items[0])

    for i in range(len(items)):
        for j in range(len(items[0])):
            out[j] += items[i][j]
            
    for i in range(len(out)):
        if out[i] > 0:
            out[i] = 1
    return out

def arr_to_sp_str(arr, sp):
    return sp.join(map(str, arr)) + sp