# hash_list_checker.py

import hashlib
import os
import sys

def hash_apk(apk_path):
    try:
        with open(apk_path, "rb") as apk:
            return hashlib.md5(apk.read()).hexdigest()
    except:
        print(apk_path, "removed by firewall!")

def is_value_existed(hash_value, list_path):
    with open(list_path, "r", encoding="utf8") as list:
        if hash_value in list.read():
            return True

def update_hash_list(apk, list_path):
    md5 = hash_apk(apk)
    package_name = apk.split(os.path.sep)[-1].split(' - ')[-1]
    folder = os.path.dirname(apk).split(os.path.sep)[-2]

    if os.path.exists(list_path) and is_value_existed(md5, list_path):
        print("apk existed: " + package_name)
    else:
        # print("write: "  + apk.split(os.path.sep)[-1])
        with open(list_path, "a+", encoding="utf8") as list:
            list.write(str(md5) + '\t' + package_name + '\t' + folder + "\n")
            return True

def main():
    folder = sys.argv[1]
    path = "C:\\Age_Rating\\App_downloader\\Downloads\\" + folder + "\\APKs\\"
    list_path = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"

    for (dirpath, dirnames, filenames) in os.walk(path):
        for name in filenames:
            apk_path = os.path.join(dirpath, name)
            update_hash_list(apk_path, list_path)

if __name__ == "__main__":
    main()