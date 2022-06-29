import argparse
import json
import os
import time
import sys

# for (dirpath, dirnames, filenames) in os.walk('/dtpishu/mph/playScraper/results'):
#     for name in filenames:

# thepath = os.path.join(dirpath, name)

#   TOP_FREE = 'topselling_free',
#   TOP_PAID = 'topselling_paid',
#   NEW_FREE = 'topselling_new_free',
#   NEW_PAID = 'topselling_new_paid',
#   GROSSING = 'topgrossing',
#   TRENDING = 'movers_shakers',
#   TOP_FREE_GAMES = 'topselling_free_games',
#   TOP_PAID_GAMES = 'topselling_paid_games',
#   TOP_GROSSING_GAMES = 'topselling_grossing_games',
#   NEW_FAMILY = 'topselling_new_family'

path = "C:\\Age_Rating\\App_downloader\\Downloads\\"

parser = argparse.ArgumentParser()
# parser.add_argument('-t', metavar='category', type=str, default='APPLICATION',
#                         help='The category of apps.')
parser.add_argument('-n', metavar='number', type=str, default='5',
                        help='The number of apps.')
# parser.add_argument('-d', metavar='detail', type=str, default='true',
#                         help='Detail info or not.')
# parser.add_argument('-c', metavar='collection', type=str, default='TOP_FREE',
#                         help='The collection of apps.')
parser.add_argument('-r', metavar='reviews', type=str, default='0',
                        help='Number of reviews to download.')
parser.add_argument('-p', metavar='path', type=str, default='0',
                        help='Path of apk folder.')
args = parser.parse_args()

category = args.t
num = args.n
collection = args.c
# reviews = args.r

os.system('node scraper_app_list.js ' + category + ' ' + collection + ' ' + num + ' ' + args.d)

path = path + "list_" + category + "_" + collection + '_'  + num + ".json"
with open(path, "r", encoding="utf8") as load_f:
    load_arr = json.load(load_f)
    
    # print(len(load_arr))

    for item in load_arr:
        appId = item["appId"]
        # name = item["title"]
        os.system('pipenv run python download.py ' + appId)
        # if reviews != '0':
        #     os.system('node scraper_reviews.js ' + appId + ' ' + reviews + ' ' + folder)
        print("done", appId)
        time.sleep(1)
        # if item["contentRating"] != 'Mature 17+' and item["contentRating"] != 'Adults only 18+':
        #     print(item["contentRating"],'|',item["title"])



