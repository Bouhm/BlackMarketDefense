__author__ = 'Bouhm'

#Program that uses methods from RiotAPIStats mainly for testing/debugging
from riot_API_data import RiotAPIData
import keys
import os.path
import urllib.request
import sys
import requests
import time

def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "en-US,en;q=0.8",
    }
    api = RiotAPIData(keys.API_KEY)
    print("Options: ")
    print("(1) Update item list")
    print("(2) Update champion list")
    option = input(':')
    if option == '1':
        item_data(api, headers)
    elif option == '2':
        champion_data(api, headers)

def item_data(api, headers):
    item_data = api._get_all_items()
    if not os.path.isfile("database/items.json"):
        file = open("database/items.json", 'w+')
        for item in item_data:
            file.write("%s  \n" % item)
    else:
        with open("database/items.json", 'a') as file:
            for item in item_data:
                file.write("%s\n" % item)

    for item in item_data:
        r = requests.get(item['img'], headers=headers)
        if r.status_code != 200:
            print("Request denied")
            sys.exit()
        urllib.request.urlretrieve(item['img'], "database/item_img/" + str(item['itemId']) + ".png")
    urllib.request.urlcleanup()

def champion_data(api, headers):
    champion_data = api.get_all_champs()

    if not os.path.isfile("database/champions.json"):
        file = open("database/champions.json", 'w+')
        for champ in champion_data:
            file.write("%s  \n" % champ)
    else:
        with open("database/champions.json", 'a') as file:
            for champ in champion_data:
                file.write("%s\n" % champ)

    for champ in champion_data:
        r = requests.get(champ['img'], headers=headers)
        if r.status_code != 200:
            print("Request denied")
            sys.exit()
        urllib.request.urlretrieve(champ['img'], "database/champ_img/" + champ['name'] + ".png")
    urllib.request.urlcleanup()

if __name__ == "__main__":
    main()
