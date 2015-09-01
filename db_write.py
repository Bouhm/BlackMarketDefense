__author__ = 'Bouhm'
#Program that uses methods from RiotAPIStats mainly for building database
#Database used for game

from riot_API_data import RiotAPIData
import data_aggr
import keys
import os.path
import urllib.request
import sys
import requests
import json
import random
import pprint
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
    print("(3) Update champion winrates")
    print("(4) Update mercenary winrates")
    print("(5) Update data from matches")
    print("(6) Update game data")
    print("(7) Condense game data")
    option = input(':')
    if option == '1':
        item_data(api, headers, False)
    elif option == '2':
        champion_data(api, headers, False)
    elif option == '3':
        champion_winrates(api)
    elif option == '4':
        merc_winrates(api)
    elif option == '5':
        data_from_matches(api, "NA", 2)
    elif option == '6':
        game_data(api, 'NA', 6000)
    else:
        condense_data()

#Get static item data and save item name, ID, and image URI to local db
def item_data(api, headers, img):
    item_data = api.get_all_items()
    if not os.path.isfile("database/items.json"):
        file = open("database/items.json", 'w+')
        #for item in item_data:
        file.write("%s  \n" % item_data)
    else:
        with open("database/items.json", 'a') as file:
            #for item in item_data:
            file.write("%s\n" % item_data)
    if(img):
        for item in item_data:
            r = requests.get(item['img'], headers=headers)
            if r.status_code != 200:
                print("Request denied")
                sys.exit()
            urllib.request.urlretrieve(item['img'], "database/item_img/" + str(item['itemId']) + ".png")
        urllib.request.urlcleanup()

#Get static champion data and store name, ID, and image URI to local db
def champion_data(api, headers, img):
    champion_data = api.get_all_champs()
    if not os.path.isfile("database/champions.json"):
        file = open("database/champions.json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % champion_data)
    else:
        with open("database/champions.json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % champion_data)

    if(img):
        for champ in champion_data:
            r = requests.get(champ['img'], headers=headers)
            if r.status_code != 200:
                print("Request denied")
                sys.exit()
            urllib.request.urlretrieve(champ['img'], "database/champ_img/" + champ['name'] + ".png")
        urllib.request.urlcleanup()

def champion_winrates(api):
    return

def merc_winrates(api):
    return

#From match data get game data and save
def game_data(api, region, num):
    game_data = data_aggr.get_game_data_format(api, region, num)
    if not os.path.isfile("database/game_data2.json"):
        file = open("database/game_data2.json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % game_data)
    else:
        with open("database/game_data.json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % game_data)
    return

#For making adjustments to wave sorting in game data
def condense_data():
    with open("database/game_data.json") as file:
        game_data = json.load(file)
    for x in range (1, 31):
        while len(game_data['wave' + str(x)]) > 10:
            game_data['wave' + str(x)].remove(game_data['wave' + str(x)][random.randint(0, len(game_data['wave' + str(x)]))])
    if not os.path.isfile("database/champions.json"):
        file = open("database/game_data_min.json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % game_data)
    else:
        with open("database/game_data_min.json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % game_data)
    return

#This method because I don't want to run a script for 3-5 hours again
def modify_waves_data():
    with open("database/game_data.json") as file:
        game_data = json.load(file)

    return


#Get data from matches, more useful for data analysis
def data_from_matches(api, region, num):
    with open("dataset/" + region + ".json") as file:
        matches_list = json.load(file)
    matches = random.sample(range(1,10000), num)
    matches_data = []
    for match in matches:
        matches_data.append(api.get_BMB_data(matches_list[match]))

    json.dumps(matches_data)
    if not os.path.isfile("database/matches_data.json"):
        file = open("database/matches_data.json", 'w+')
        for match in matches_data:
            file.write("%s  \n" % match)
    else:
        with open("database/matches_data.json", 'a') as file:
            for match in matches_data:
                file.write("%s\n" % match)
    return

#Convert all ids in python dictionary into names, key and value pairs are appropriately replaced
def id_to_name(dict):
    with open("database/items.json") as file:
        item_data = json.load(file)
    with open("database/champions.json") as file:
        champ_data = json.load(file)
    for team in dict.values():
        for key, value in team.items():
            if key == 'champions':
                for champion in team[key]:
                    for champ in champ_data:
                        if champion['championId'] == champ['championId']:
                            champion['name'] = champ['name']
                    for champ in champ_data:
                        champion.pop('championId', None)
                    for item in champion['items']:
                        for item_name in item_data:
                            if item == item_name['itemId']:
                                champion['items'].append(item_name['name'])
                    champion['items'] = [x for x in champion['items'] if not isinstance(x, int)]
    return dict

if __name__ == "__main__":
    main()
