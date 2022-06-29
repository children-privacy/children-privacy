# case_downloaer.py

import json
import os
import time
# from app_review_downloader import download_app_and_review

case_list_raw = r"C:\Age_Rating\Apk\Apk_list\case_list_raw.txt"
case_list = r"C:\Age_Rating\Apk\Apk_list\case_list.txt"
case_json = r"C:\Age_Rating\Apk\Apk_list\case_list.json"
save_path = r"C:\Age_Rating\App_downloader\Downloads"
reviews = '3000'

def gen_list():
    list = []
    with open(case_list_raw, "r", encoding="utf-8") as f:
        for line in f:
            line = line.split("=")[-1].replace('\n','')
            list.append({"appId":line})

    with open(case_json, 'w+', encoding='utf-8') as f:
        json.dump(list,f)

def download_app_and_review(path_json, reviews, folder_path):
    '''
    path_json: The path of app list
    reviews: number of reviews to download
    folder_path: app saving folder
    '''
    with open(path_json, "r", encoding="utf8") as load_f:
        load_arr = json.load(load_f)

        for item in load_arr:
            appId = item["appId"]
            os.system('pipenv run python download.py ' + appId)
            if reviews != '0':
                os.system('node scraper_reviews.js ' + appId + ' ' + reviews + ' ' + folder_path)
            print("done", appId)
            time.sleep(1)

gen_list()
download_app_and_review(case_json, reviews, save_path)
