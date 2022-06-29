# folder_content_checker.py

import os
import sys

def check_folder_content(source, target):
    for (dirpath, dirnames, filenames) in os.walk(source):
        filenames_source = filenames
        # print(filenames_source)
    
    for (dirpath, dirnames, filenames) in os.walk(target):
        filenames_target = filenames

    for filename in filenames_source:
        if filename.split(' - ')[-1] not in filenames_target:
            print(filename)

def rename_apk(folder):
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for filename in filenames:
            apk = os.path.join(dirpath, filename)
            apk_new = os.path.join(dirpath, filename.split(' - ')[-1])
            os.rename(apk, apk_new)

def main():
    source = "C:\Age_Rating\App_downloader\Downloads\Application_NewFree_1Mar2021_86\APKs"
    target = "C:\Age_Rating\App_downloader\Downloads\APPLICATION_NEW_FREE_21Mar2021_126\APKs"

    source  = sys.argv[1]

    # print(source)

    # check_folder_content(source, target)
    rename_apk(source)


if __name__ == "__main__":
    main()