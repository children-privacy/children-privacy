# app_downloader.py

import argparse
import json
import os
import time
import sys

# for (dirpath, dirnames, filenames) in os.walk('/dtpishu/mph/playScraper/results'):
#     for name in filenames:

# thepath = os.path.join(dirpath, name)

# path = "C:\\Age_Rating\\App_downloader\\Downloads\\"

# parser = argparse.ArgumentParser()
# parser.add_argument('-t', metavar='CATEGORY', type=str, default='APPLICATION', help='The category of apps.')
# parser.add_argument('-n', metavar='NUMBER', type=str, default='200', help='The number of apps.')
# parser.add_argument('-c', metavar='COLLECTION', type=str, default='TOP_FREE', help='The collection of apps.')
# parser.add_argument('-r', metavar='N_REVIEWS', type=str, default='3000', help='Number of reviews to download.')
# args = parser.parse_args()

# category = args.t
# num = args.n
# collection = args.c
# reviews = args.r

path = "C:\\Users\\User\\Dropbox\\Research\\Finished project\\Contact-Tracing-Apps\\New_versions_apk\\app_list.txt"

with open(path, "r", encoding="utf8") as load_f:
    for package_name in load_f:
        package_name = package_name[:-1]
        os.system('pipenv run python download.py ' + package_name)

# os.system('node scraper_app_list.js ' + category + ' ' + collection + ' ' + num + ' ' + path)
# path_json = path + "App_list\\" + os.listdir(path + "App_list\\")[0]

# with open(path_json, "r", encoding="utf8") as load_f:
#     load_arr = json.load(load_f)
    
#     # print(len(load_arr))

#     for item in load_arr:
#         appId = item["appId"]
#         # name = item["title"]
#         os.system('pipenv run python download.py ' + appId)
#         if reviews != '0':
#             os.system('node scraper_reviews.js ' + appId + ' ' + reviews + ' ' + path)
#         print("done", appId)
#         time.sleep(1)
        # if item["contentRating"] != 'Mature 17+' and item["contentRating"] != 'Adults only 18+':
        #     print(item["contentRating"],'|',item["title"])

# TOP_FREE = 'topselling_free',
# TOP_PAID = 'topselling_paid',
# NEW_FREE = 'topselling_new_free',
# NEW_PAID = 'topselling_new_paid',
# GROSSING = 'topgrossing',
# TRENDING = 'movers_shakers',
# TOP_FREE_GAMES = 'topselling_free_games',
# TOP_PAID_GAMES = 'topselling_paid_games',
# TOP_GROSSING_GAMES = 'topselling_grossing_games',
# NEW_FAMILY = 'topselling_new_family'

# APPLICATION = 'APPLICATION',
# ANDROID_WEAR = 'ANDROID_WEAR',
# ART_AND_DESIGN = 'ART_AND_DESIGN',
# AUTO_AND_VEHICLES = 'AUTO_AND_VEHICLES',
# BEAUTY = 'BEAUTY',
# BOOKS_AND_REFERENCE = 'BOOKS_AND_REFERENCE',
# BUSINESS = 'BUSINESS',
# COMICS = 'COMICS',
# COMMUNICATION = 'COMMUNICATION',
# DATING = 'DATING',
# EDUCATION = 'EDUCATION',
# ENTERTAINMENT = 'ENTERTAINMENT',
# EVENTS = 'EVENTS',
# FINANCE = 'FINANCE',
# FOOD_AND_DRINK = 'FOOD_AND_DRINK',
# HEALTH_AND_FITNESS = 'HEALTH_AND_FITNESS',
# HOUSE_AND_HOME = 'HOUSE_AND_HOME',
# LIBRARIES_AND_DEMO = 'LIBRARIES_AND_DEMO',
# LIFESTYLE = 'LIFESTYLE',
# MAPS_AND_NAVIGATION = 'MAPS_AND_NAVIGATION',
# MEDICAL = 'MEDICAL',
# MUSIC_AND_AUDIO = 'MUSIC_AND_AUDIO',
# NEWS_AND_MAGAZINES = 'NEWS_AND_MAGAZINES',
# PARENTING = 'PARENTING',
# PERSONALIZATION = 'PERSONALIZATION',
# PHOTOGRAPHY = 'PHOTOGRAPHY',
# PRODUCTIVITY = 'PRODUCTIVITY',
# SHOPPING = 'SHOPPING',
# SOCIAL = 'SOCIAL',
# SPORTS = 'SPORTS',
# TOOLS = 'TOOLS',
# TRAVEL_AND_LOCAL = 'TRAVEL_AND_LOCAL',
# VIDEO_PLAYERS = 'VIDEO_PLAYERS',
# WEATHER = 'WEATHER',
# GAME = 'GAME',
# GAME_ACTION = 'GAME_ACTION',
# GAME_ADVENTURE = 'GAME_ADVENTURE',
# GAME_ARCADE = 'GAME_ARCADE',
# GAME_BOARD = 'GAME_BOARD',
# GAME_CARD = 'GAME_CARD',
# GAME_CASINO = 'GAME_CASINO',
# GAME_CASUAL = 'GAME_CASUAL',
# GAME_EDUCATIONAL = 'GAME_EDUCATIONAL',
# GAME_MUSIC = 'GAME_MUSIC',
# GAME_PUZZLE = 'GAME_PUZZLE',
# GAME_RACING = 'GAME_RACING',
# GAME_ROLE_PLAYING = 'GAME_ROLE_PLAYING',
# GAME_SIMULATION = 'GAME_SIMULATION',
# GAME_SPORTS = 'GAME_SPORTS',
# GAME_STRATEGY = 'GAME_STRATEGY',
# GAME_TRIVIA = 'GAME_TRIVIA',
# GAME_WORD = 'GAME_WORD',
# FAMILY = 'FAMILY',
# FAMILY_ACTION = 'FAMILY_ACTION',
# FAMILY_BRAINGAMES = 'FAMILY_BRAINGAMES',
# FAMILY_CREATE = 'FAMILY_CREATE',
# FAMILY_EDUCATION = 'FAMILY_EDUCATION',
# FAMILY_MUSICVIDEO = 'FAMILY_MUSICVIDEO',
# FAMILY_PRETEND = 'FAMILY_PRETEND'