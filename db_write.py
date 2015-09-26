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
from pprint import pprint
import time
import math

def main():
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5)",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "accept-encoding": "gzip,deflate,sdch",
        "accept-language": "en-US,en;q=0.8",
    }
    print("Choose region: ")
    region = input(': ')
    api = RiotAPIData(keys.API_KEY, region)
    print("")
    print("Options: ")
    print("(1) Update item list")
    print("(2) Update champion list")
    print("(3) Update data from matches")
    print("(4) Get winrates")
    print("(5) Combine winrate data")
    print("(6) Update game data")
    print("(7) Overflow data")
    print("(8) Condense data")
    option = input(':')
    if option == '1':
        item_data(api, headers, False)
    elif option == '2':
        champion_data(api, headers, False)
    elif option == '3':
        data_from_matches(api, region, 2)
    elif option == '4':
        get_winrates(region)
    elif option == '5':
        combine_winrate_data('na', 'euw')
    elif option == '6':
        game_data(api, region, 10, 20, 1)
    elif option == '7':
        overflow_data(20)
    elif option == '8':
        condense_data(20)

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

#From match data get game data and save
def game_data(api, region, num, totalWaves, local):
    game_data = json.dumps(data_aggr.get_game_data_format(api, region, num, totalWaves, local))
    if not os.path.isfile("database/game_data_" + region + ".json"):
        file = open("database/game_data_" + region + ".json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % game_data)
    else:
        with open("database/game_data_" + region + ".json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % game_data)
    return

#For making adjustments to wave sorting in game data
def condense_data(max):
    with open("database/game_data.json") as file:
        game_data = json.load(file)
    for x in range (1, 21):
        size = len(game_data['wave' + str(x)])
        while len(game_data['wave' + str(x)]) > max:
            index = random.randint(0, size - 1)
            game_data['wave' + str(x)].remove(game_data['wave' + str(x)][index])
            size -= 1
    game_data = json.dumps(game_data)
    if not os.path.isfile("database/game_data_min.json"):
        file = open("database/game_data_min.json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % game_data)
    else:
        with open("database/game_data_min.json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % game_data)
    return

#This method because I don't want to run a script for 3-5 hours again
def overflow_data(numMatches):
    with open("database/game_data2.json") as file:
        game_data = json.load(file)
    di_size = len(game_data.keys())
    #matches = game_data.copy()

    for x in range (1, 20):
        list_size = len(game_data['wave' + str(21 - x)])
        for y in range (1, math.floor(list_size/2) + 1):
            data = game_data['wave' + str(21 - x)].pop()
            if 'wave' + str(20 - x) not in game_data.keys():
                game_data.update({'wave' + str(20 - x): [data]})
            else:
                game_data['wave' + str(20 - x)].insert(0, data)
    game_data = json.dumps(game_data)
    if not os.path.isfile("database/game_data_OF.json"):
        file = open("database/game_data_OF.json", 'w+')
        #for champ in champion_data:
        file.write("%s  \n" % game_data)
    else:
        with open("database/game_data_OF.json", 'a') as file:
            #for champ in champion_data:
            file.write("%s\n" % game_data)
    return

#Get data from matches, more useful for data analysis
def data_from_matches(api, region, num):
    with open("dataset/" + region + ".json") as file:
        matches_list = json.load(file)
    matches = random.sample(range(1,10000), num)
    matches_data = []
    matches_data_s = []
    for x in range (1, 10000):
        try:
            match_data = json.dumps(api.get_BMB_data(matches_list[x]))
            matches_data.append(match_data)
            time.sleep(1.3)
        except:
            pass

    if not os.path.isfile("database/matches_data_" + region + ".json"):
        file = open("database/matches_data_" + region + " .json", 'w+')
        file.write("%s  \n" % matches_data)
    else:
        with open("database/matches_data_" + region + ".json", 'a') as file:
            file.write("%s\n" % matches_data)
    return

#Convert all ids in python dictionary into names, key and value pairs are appropriately replaced
def id_to_name(dict):
    with open("database/items.json") as file:
        item_data = json.load(file)
    with open("database/champions.json") as file:
        champ_data = json.load(file)
    for x in range (1, 3):
        team = dict[str(x*100)]
        for key, value in team.items():
            if key == 'champions':
                for champion in team[key]:
                    for champ in champ_data:
                        if 'championId' in champion.keys() and champion['championId'] == champ['championId']:
                            champion['name'] = champ['name']
                    for champ in champ_data:
                        champion.pop('championId', None)
                    for item in champion['items']:
                        for item_name in item_data:
                            if item == item_name['itemId']:
                                champion['items'].append(item_name['name'])
                    champion['items'] = [x for x in champion['items'] if not isinstance(x, int)]
            else:
                for item in item_data:
                    if item['itemId'] == key:
                        team.update({item['name']:team[key]})
                        del team[key]
    return dict

def get_winrates(region):
    winrate_data = data_aggr.winrate_data(region)
    winrate_data = json.dumps(winrate_data)
    if not os.path.isfile("database/winrate_data_" + region + ".json"):
        file = open("database/winrate_data_" + region + ".json", 'w+')
        #pprint(winrate_data, stream=file)
        file.write("%s  \n" % winrate_data)
    else:
        with open("database/winrate_data_" + region + ".json", 'a') as file:
            #pprint(winrate_data, stream=file)
            file.write("%s \n" % winrate_data)
    return

def format_data():
    with open("database/matches_data_id.json", 'r') as file:
        BMB_data = json.load(file)
    if not os.path.isfile("database/matches_data_list.json"):
        file = open("database/matches_data_list.json", 'w+')
        for datum in BMB_data:
            if not os.path.isfile("database/matches_data_list.json"):
                file = open("database/matches_data_list.json", 'w+')
                file.write("%s  \n" % datum + ",")
        else:
            with open("database/matches_data_list.json", 'a') as file:
                for datum in BMB_data:
                    file.write("%s\n" % datum + ",")
    return

def combine_winrate_data(region1, region2):
    with open("database/winrate_data_" + region1 + ".json", 'r') as file:
        wr_data1 = json.load(file)
    with open("database/winrate_data_" + region2 + ".json", 'r') as file:
        wr_data2 = json.load(file)
    wr_data = wr_data1.copy()

    for champion in wr_data1['champions']:
        if champion in wr_data2['champions'].keys():
            wr_data['champions'][champion]['games'] += wr_data2['champions'][champion]['games']
            wr_data['champions'][champion]['wins'] += wr_data2['champions'][champion]['wins']
            wr_data['champions'][champion]['winrate'] = wr_data['champions'][champion]['wins']/wr_data['champions'][champion]['games']
        else:
            wr_data['champions'][champion] = wr_data2['champions'][champion]

    for mercenary in wr_data1['mercenaries']:
        if mercenary in wr_data2['mercenaries'].keys():
            wr_data['mercenaries'][mercenary]['wins'] += wr_data2['mercenaries'][mercenary]['wins']
            wr_data['mercenaries'][mercenary]['games'] += wr_data2['mercenaries'][mercenary]['games']
            wr_data['mercenaries'][mercenary]['winrate'] = wr_data['mercenaries'][mercenary]['wins']/ wr_data['mercenaries'][mercenary]['games']
            for stats in wr_data1['mercenaries'][mercenary]:
                if stats in wr_data2['mercenaries'].keys():
                    wr_data['mercenaries'][mercenary][stats]['games'] += wr_data2['mercenaries'][mercenary][stats]['games']
                    wr_data['mercenaries'][mercenary][stats]['wins'] += wr_data2['mercenaries'][mercenary][stats]['wins']
                    wr_data['mercenaries'][mercenary][stats]['winrate'] = wr_data['mercenaries'][mercenary][stats]['wins']/wr_data['mercenaries'][mercenary][stats]['games']
                else:
                    wr_data['mercenaries'][mercenary][stats] = wr_data2['mercenaries'][mercenary][stats]

    if not os.path.isfile("database/winrate_data_" + region1 + region2 + ".json"):
        file = open("database/winrate_data_" + region1 + region2 + ".json", 'w+')
        pprint(wr_data, stream=file)
        #file.write("%s  \n" % winrate_data)
    else:
        with open("database/winrate_data_" + region1 + region2 + ".json", 'a') as file:
            pprint(wr_data, stream=file)
            #file.write("%s \n" % winrate_data)

if __name__ == "__main__":
    main()
