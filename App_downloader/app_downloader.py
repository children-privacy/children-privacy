# app_downloader.py

import argparse
import os
import shutil
import sys

import misc
from app_review_downloader import (download_app_and_review, download_app_apkpure, obtain_app_list)
from duplicate_remover import remove_duplicate_apk


class App_downloader:
    hash_list = r"C:\Age_Rating\Apk\Apk_list\apk_list.txt"
    save_path = r"C:\Age_Rating\App_downloader\Downloads"
    type = 'TOP_FREE'
    n_apps = 200
    n_reviews = 3000
    store = ''
    app_list = ''
    category = ''

    def __init__(self, store, app_list, category):
        self.set_store(store)
        self.set_app_list(app_list)
        self.set_category(category)
        
    def download_by_category(self, category):
        if category == 'APPLICATION':
            self.type = 'NEW_FREE'
        elif category == 'NEW_FAMILY':
            category = 'FAMILY'
            self.type = 'NEW_FAMILY'

        app_list = obtain_app_list(category, self.type, str(self.n_apps), self.save_path)
        download_app_and_review(app_list, str(self.n_reviews), self.save_path)
        self.clean_up(category)

    def download_by_app_list(self): 
        category = '_'.join(self.app_list.split(os.path.sep)[-1].split('_')[1:-3])
        download_app_and_review(self.app_list, str(self.n_reviews), self.save_path)
        self.clean_up(category)

    def download_by_app_list_apkpure(self):
        category = '_'.join(self.app_list.split(os.path.sep)[-1].split('_')[1:-3])
        download_app_apkpure(self.app_list, self.save_path)

    def clean_up(self, category):  
        save_path = self.save_path + os.path.sep + category + '_' + self.type + '_' + misc.get_date()
        os.mkdir(save_path)
        os.mkdir(save_path + os.path.sep + 'APKs')

        if os.path.exists(self.save_path + os.path.sep + 'App_list'):
            shutil.move(self.save_path + os.path.sep + 'App_list', save_path)
        if os.path.exists(self.save_path + os.path.sep + 'Reviews'): 
            shutil.move(self.save_path + os.path.sep + 'Reviews', save_path)

        for (dirpath, dirnames, filenames) in os.walk(self.save_path):
            for filename in filenames:
                apk_path = os.path.join(self.save_path, filename)
                if os.path.exists(apk_path):
                    shutil.move(apk_path, save_path + os.path.sep + 'APKs')
        apk_folder = save_path + os.path.sep + 'APKs'
        remove_duplicate_apk(apk_folder, self.hash_list)
        misc.rename_folder_by_size(save_path, misc.get_n_files(apk_folder))

    def start_download(self):
        if self.app_list == '':
            if self.category == '':                     
                for category in self.categories:
                    self.download_by_category(category)     # download by categories
            else:                                           # download a specific category
                self.download_by_category(self.category)
        elif self.category == '':                           # download by app list
            if self.store == 'google':
                self.download_by_app_list()
            elif self.store == 'apkpure':
                self.download_by_app_list_apkpure()

    def set_store(self, store):
        if store:
            self.store = store

    def set_app_list(self, app_list):
        if app_list:
            self.app_list = app_list

    def set_category(self, category):
        if category:
            self.category = category

    categories = [
        # 'ANDROID_WEAR',
        # 'ART_AND_DESIGN',
        # 'AUTO_AND_VEHICLES',
        # 'BEAUTY',
        # 'BOOKS_AND_REFERENCE',
        # 'BUSINESS',
        # 'COMICS',
        # 'COMMUNICATION',
        # 'DATING',
        # 'EDUCATION',
        # 'ENTERTAINMENT',
        # 'EVENTS',
        # 'FINANCE',
        # 'FOOD_AND_DRINK',
        # 'HEALTH_AND_FITNESS',
        # 'HOUSE_AND_HOME',
        # 'LIBRARIES_AND_DEMO',
        # 'LIFESTYLE',
        # 'MAPS_AND_NAVIGATION',
        # 'MEDICAL',
        # 'MUSIC_AND_AUDIO',
        # 'NEWS_AND_MAGAZINES',
        # 'PARENTING',
        # 'PERSONALIZATION',
        # 'PHOTOGRAPHY',
        # 'PRODUCTIVITY',
        # 'SHOPPING',
        # 'SOCIAL',
        # 'SPORTS',
        # 'TOOLS',
        # 'TRAVEL_AND_LOCAL',
        # 'VIDEO_PLAYERS',
        # 'WEATHER',
        'FAMILY',
        'NEW_FAMILY'
        # 'APPLICATION'
    ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', metavar='APP_LIST', type=str, help='The path to app_list.')
    parser.add_argument('-s', metavar='STORE', type=str, default='google', help='The app store, google or apkpure.')
    parser.add_argument('-c', metavar='CATEGORY', type=str, help='The category of app.')
    args = parser.parse_args()

    App_downloader(args.s, args.l, args.c).start_download()
    # App_downloader(args.s, args.l, args.c).clean_up('APPLICATION')

if __name__ == "__main__":
    main()
