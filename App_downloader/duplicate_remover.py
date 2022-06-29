# duplicate_remover.py

import os
import sys
from hash_list_checker import update_hash_list

def remove_duplicate_apk(folder, hash_list):
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for name in filenames:
            if os.path.splitext(name)[-1] == ".apk":
                apk_path = os.path.join(dirpath, name)
                if os.path.exists(apk_path):
                    if not update_hash_list(apk_path, hash_list):
                        os.remove(apk_path)
                        print("apk removed")

def main():
    path = sys.argv[1]
    # path = "C:\\Age_Rating\\App_downloader\\Downloads\\" + folder + "\\APKs\\"
    # path = "C:\Age_Rating\App_downloader\Downloads\ANDROID_WEAR_TOP_TOP_FREE_19Mar2021_185\APKs"
    hash_list = "C:\\Age_Rating\\Apk\\Apk_list\\apk_list.txt"

    remove_duplicate_apk(path, hash_list)

if __name__ == "__main__":
    main()