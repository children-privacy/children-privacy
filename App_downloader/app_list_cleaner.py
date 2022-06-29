# app_list_cleaner.py

import os
import argparse
import json
from hash_list_checker import is_value_existed

def clean_app_list(app_list, hash_list):
    with open(app_list, "r", encoding="utf8") as f_app_list:
        apps = []
        counter = 0
        arr_app_json = json.load(f_app_list)
        for app in arr_app_json:
            package_name = app['appId'] + '.apk'
            if is_value_existed(package_name, hash_list):
                apps.append(app)
                counter += 1
    with open(app_list, "w", encoding="utf8") as f_app_list:
        json.dump(apps, f_app_list)
    print(counter, '\t', app_list.split(os.path.sep)[-1])

def clean_all_app_list(path, hash_list):
    for (dirpath, dirnames, filenames) in os.walk(path):
        if dirpath.split(os.path.sep)[-1] == "App_list":
            for filename in filenames:
                if filename.split('_')[0] == "list":
                    clean_app_list(dirpath + '\\' + filename, hash_list)


def main():
    hash_list = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"
    path = "C:\\Age_Rating\\App_downloader\\Downloads"

    clean_all_app_list(path, hash_list)

if __name__ == "__main__":
    main()

