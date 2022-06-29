# privacy_policy_from_hash_list.py

import argparse
import os
import sys

def get_policy_info(hash_list):
    with open(hash_list, "r", encoding="utf8") as f_hash_list:
        for line in f_hash_list:
            package_name = line.split('\t')[-1]
            os.system('node scraper_search.js ' + appId)

def main():
    hash_list = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', metavar='HASH_LIST', type=str, default=hash_list, help='The path of hash list.')
    args = parser.parse_args()

    hash_list = args.l

    get_policy_info(hash_list)


if __name__ == "__main__":
    main()