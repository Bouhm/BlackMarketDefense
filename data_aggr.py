__author__ = 'Bouhm'
#Program that uses methods from RiotAPIStats for data aggregation
#For data analysis and data format for game

from riot_API_data import RiotAPIData
import keys
import pprint
import json
import random
import math
import time

def main():
    api = RiotAPIData(keys.API_KEY)
    pprint.pprint(get_game_data_format(api, 'NA', 100, 20))

#Convert all ids to names in python dictionary, key value pairs are appropriately replaced
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

#From match data get game data
def get_game_data_format(api, region, num, totalWaves):
    with open("dataset/" + region + ".json") as file:
        matches_list = json.load(file)
    matches = random.sample(range(1,10000), num)
    matches_data = []
    all_waves = {}

    for x in range (1, 10000):
    #for match in matches:
        try:
            matches_data.append(id_to_name(api.get_BMB_data(matches_list[x])))
            time.sleep(1.3)
        except:
            pass

    for match in matches_data:
        team = match['100']
        wave = match['200']
        stats = 0
        upgrades = 0
        count = 0
        waves = {}
        champions = []
        towers = []
        merc_wave = wave.copy()
        mercs = team.copy()
        del merc_wave['winner']
        del merc_wave['champions']
        del mercs['winner']
        del mercs['champions']
        merc_wave.update({'mercs': mercs})

        for champion in wave['champions']:
            if 'name' in champion.keys():
                champions.append(champion['name'])
        merc_wave.update({'champions': champions})

        for champion in team['champions']:
            if 'name' in champion.keys():
                towers.append(champion['name'])

        #WAVE SORTING ALGORITHM (BASED ON UPGRADES & NUMBER OF MERCS AND RESPECTIVE DISTRIBUTION (SUPER BASIC))
        #Currently only optimized for 20
        if 'Ironback' in wave.keys():
            count += len(wave['Ironback'])
            for upgrade in wave['Ironback']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade'] * 2
        if 'Razorfin' in wave.keys():
            count += len(wave['Razorfin'])
            for upgrade in wave['Razorfin']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade'] * 2
        if 'Ocklepod' in wave.keys():
            count += len(wave['Ocklepod'])
            for upgrade in wave['Ocklepod']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade'] * 2
        if 'Plundercrab' in wave.keys():
            count += len(wave['Plundercrab'])
            for upgrade in wave['Plundercrab']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade'] * 2

        if count > 3:
            x = 0
            for waveNum in range (1, totalWaves + 1):
                if stats + upgrades <= x:
                    k = "wave" + str(waveNum)
                    break
                x += 3
            waves.update({'wave': merc_wave})
            waves.update({'towers': towers})
            waves.update({'matchId': match['matchId']})
            if k in all_waves.keys():
                all_waves[k].append(waves)
            else:
                all_waves.update({k: [waves]})
    return json.dumps(all_waves)

#For data analysis
def winrate_data(region):
    with open("database/items.json") as file:
        item_data = json.load(file)
    with open("database/champions.json") as file:
        champ_data = json.load(file)
    with open("database/matches_data_" + region + ".json", 'r') as file:
        BMB_data = json.load(file)
    champion_wr = {}
    mercenary_wr = {}
    item_wr = {}
    #mercs = {"3611":"Razorfin", "3612":"Ironback", "3613":"Plundercrab", "3614":"Ocklepod"}
    for match in BMB_data:
        for x in range (1, 3):
            if match[str(x * 100)]['winner'] == "True":
                win = 1
            else:
                win = 0

            for champion in match[str(x * 100)]['champions']:
                for champ in champ_data:
                    if champion['championId'] == champ['championId']:
                        if champ['name'] not in champion_wr.keys():
                            champion_wr.update({champ['name']:{'wins':1, 'games':1, 'winrate':win}})
                        else:
                            champion_wr[champ['name']]['wins'] += win
                            champion_wr[champ['name']]['games'] += 1
                            champion_wr[champ['name']]['winrate'] = champion_wr[champ['name']]['wins']/champion_wr[champ['name']]['games']
                for item in champion['items']:
                    for item_name in item_data:
                        if item == item_name['itemId']:
                            if item_name['name'] not in item_wr.keys():
                                item_wr.update({item_name['name']:{'wins':1, 'games':1, 'winrate':win}})
                            else:
                                item_wr[item_name['name']]['wins'] += win
                                item_wr[item_name['name']]['games'] += 1
                                item_wr[item_name['name']]['winrate'] = item_wr[item_name['name']]['wins']/item_wr[item_name['name']]['games']
            if '3611' in match[str(x * 100)].keys():
                for stats in match[str(x * 100)]['3611']:
                    k = "off: " + str(stats['offense']) + ", def: " + str(stats['defense']) + ", upg: " + str(stats['upgrade'])
                    if 'Razorfin' not in mercenary_wr.keys():
                        mercenary_wr.update({'Razorfin':{'wins':win, 'games':1, 'winrate':win, k:{'wins':win, 'games':1, 'winrate':win}}})
                    else:
                        mercenary_wr['Razorfin']['wins'] += win
                        mercenary_wr['Razorfin']['games'] += 1
                        mercenary_wr['Razorfin']['winrate'] = mercenary_wr['Razorfin']['wins']/mercenary_wr['Razorfin']['games']
                        if k not in  mercenary_wr['Razorfin'].keys():
                            mercenary_wr['Razorfin'].update({k:{'wins':win, 'games':1, 'winrate':win}})
                        else:
                            mercenary_wr['Razorfin'][k]['wins'] += win
                            mercenary_wr['Razorfin'][k]['games'] += 1
                            mercenary_wr['Razorfin'][k]['winrate'] = mercenary_wr['Razorfin'][k]['wins']/ mercenary_wr['Razorfin'][k]['games']
                #mercenary_wr['Razorfin'][k].sort(key=lambda e: e['winrate'])
            if '3612' in match[str(x * 100)].keys():
                for stats in match[str(x * 100)]['3612']:
                    k = "off: " + str(stats['offense']) + ", def: " + str(stats['defense']) + ", upg: " + str(stats['upgrade'])
                    if 'Ironback' not in mercenary_wr.keys():
                        mercenary_wr.update({'Ironback':{'wins':win, 'games':1, 'winrate':win, k:{'wins':win, 'games':1, 'winrate':win}}})
                    else:
                        mercenary_wr['Ironback']['wins'] += win
                        mercenary_wr['Ironback']['games'] += 1
                        mercenary_wr['Ironback']['winrate'] = mercenary_wr['Ironback']['wins']/mercenary_wr['Ironback']['games']
                        if k not in  mercenary_wr['Ironback'].keys():
                            mercenary_wr['Ironback'].update({k:{'wins':win, 'games':1, 'winrate':win}})
                        else:
                            mercenary_wr['Ironback'][k]['wins'] += win
                            mercenary_wr['Ironback'][k]['games'] += 1
                            mercenary_wr['Ironback'][k]['winrate'] = mercenary_wr['Ironback'][k]['wins']/ mercenary_wr['Ironback'][k]['games']
                    #mercenary_wr['Ironback'][k].sort(key=lambda e: e['winrate'])
            if '3613' in match[str(x * 100)].keys():
                for stats in match[str(x * 100)]['3613']:
                    k = "off: " + str(stats['offense']) + ", def: " + str(stats['defense']) + ", upg: " + str(stats['upgrade'])
                    if 'Plundercrab' not in mercenary_wr.keys():
                        mercenary_wr.update({'Plundercrab':{'wins':win, 'games':1, 'winrate':win, k:{'wins':win, 'games':1, 'winrate':win}}})
                    else:
                        mercenary_wr['Plundercrab']['wins'] += win
                        mercenary_wr['Plundercrab']['games'] += 1
                        mercenary_wr['Plundercrab']['winrate'] = mercenary_wr['Plundercrab']['wins']/mercenary_wr['Plundercrab']['games']
                        if k not in  mercenary_wr['Plundercrab'].keys():
                            mercenary_wr['Plundercrab'].update({k:{'wins':win, 'games':1, 'winrate':win}})
                        else:
                            mercenary_wr['Plundercrab'][k]['wins'] += win
                            mercenary_wr['Plundercrab'][k]['games'] += 1
                            mercenary_wr['Plundercrab'][k]['winrate'] = mercenary_wr['Plundercrab'][k]['wins']/ mercenary_wr['Plundercrab'][k]['games']
                #mercenary_wr['Plundercrab'][k].sort(key=lambda e: e['winrate'])
            if '3614' in match[str(x * 100)].keys():
                for stats in match[str(x * 100)]['3614']:
                    k = "off: " + str(stats['offense']) + ", def: " + str(stats['defense']) + ", upg: " + str(stats['upgrade'])
                    if 'Ocklepod' not in mercenary_wr.keys():
                        mercenary_wr.update({'Ocklepod':{'wins':win, 'games':1, 'winrate':win, k:{'wins':win, 'games':1, 'winrate':win}}})
                    else:
                        mercenary_wr['Ocklepod']['wins'] += win
                        mercenary_wr['Ocklepod']['games'] += 1
                        mercenary_wr['Ocklepod']['winrate'] = mercenary_wr['Ocklepod']['wins']/mercenary_wr['Ocklepod']['games']
                        if k not in  mercenary_wr['Ocklepod'].keys():
                            mercenary_wr['Ocklepod'].update({k:{'wins':win, 'games':1, 'winrate':win}})
                        else:
                            mercenary_wr['Ocklepod'][k]['wins'] += win
                            mercenary_wr['Ocklepod'][k]['games'] += 1
                            mercenary_wr['Ocklepod'][k]['winrate'] = mercenary_wr['Ocklepod'][k]['wins']/ mercenary_wr['Ocklepod'][k]['games']
                #mercenary_wr['Ocklepod'][k].sort(key=lambda e: e['winrate'])
    return ({'champions':champion_wr, 'mercenaries':mercenary_wr, 'items':item_wr})

def match_ids(region):
    return

if __name__ == "__main__":
    main()
