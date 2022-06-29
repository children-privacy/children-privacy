# app_list_converter.py

import os
import argparse
import json

def extract_app_info(app_list, count_policy=0, count_no_policy=0, low_rating=0, high_rating=5,split='||'):
    with open(app_list, "r", encoding="utf8") as load_f:
        load_arr = json.load(load_f)
        app_info = []
        
        for app in load_arr:
            if 'privacyPolicy' in app.keys() and 'contentRating' in app.keys():
                # count_policy += 1
                if app['contentRating'] in age_ratings: 
                    app_info.append(app['title'] + split + app['appId'] + split + app['privacyPolicy'] + split + app['contentRating'] + split + app['genre'])
            else:
                count_no_policy += 1  

        return app_info

def write_to_file(path, array):
    with open(path,'w',encoding="utf8") as out_f:
        for line in array:
            if line: 
                out_f.write(line)
                out_f.write("\n")

def convert_app_list(output_path, input_list):
    write_to_file(output_path, extract_app_info(input_list))

def convert_all_app_list(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        if dirpath.split(os.path.sep)[-1] == "App_list":
            for filename in filenames:
                if filename.split('_')[0] == "list":
                    input_list = dirpath + '\\' + filename
                    output_path = os.path.dirname(input_list) + '\\app_info.txt'
                    convert_app_list(output_path, input_list)

def main():
    path = "C:\Age_Rating\App_downloader\Family_apk"

    convert_all_app_list(path)

age_ratings = [
    # 'Manga 18+',
    # 'Mature 17+',
    'Teen',
    'Everyone 10+',
    'Everyone',
]

if __name__ == "__main__":
    main()