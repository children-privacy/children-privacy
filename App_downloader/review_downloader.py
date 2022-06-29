# review_downloader.py

import argparse
import json
import os
import time
import sys

def download_reviews(list, n_reviews, o_path):
    with open(list, "r", encoding="utf8") as list_f:
        list_arr = json.load(list_f)
        for item in list_arr:
            appId = item["appId"]
            os.system('node scraper_reviews.js ' + appId + ' ' + n_reviews + ' ' + o_path)
            time.sleep(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', metavar='NUMBER', type=str, default='3000', help='The number of reviews.')
    parser.add_argument('-l', metavar='APP_LIST', type=str, required=True, help='The path of app list.')
    args = parser.parse_args()

    list = args.l
    n_reviews = args.n

    print(list.split(os.path.sep)[-1].split('.')[0])

    o_path = "C:\\Age_Rating\\App_downloader\\Downloads\\" + list.split(os.path.sep)[-1].split('.')[0] + '_'

    download_reviews(list, n_reviews, o_path)

if __name__ == "__main__":
    main()