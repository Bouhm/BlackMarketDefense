__author__ = 'Bouhm'
#Program that uses methods from RiotAPIStats for data aggregation

from riot_API_data import RiotAPIData
import keys
import pprint
import json
import random
import math
import time

def main():
    api = RiotAPIData(keys.API_KEY)
    pprint.pprint(get_game_data_format(api, 'NA', 5))

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

def get_game_data_format(api, region, num):
    with open("dataset/" + region + ".json") as file:
        matches_list = json.load(file)
    matches = random.sample(range(1,10000), num)
    matches_data = []
    all_waves = {}
    for match in matches:
        try:
            matches_data.append(id_to_name(api.get_BMB_data(matches_list[match])))
            time.sleep(1.5)
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
        merc_wave.update({'mercs': merc_wave})

        for champion in wave['champions']:
            if 'name' in champion.keys():
                champions.append(champion['name'])
        merc_wave.update({'champions': champions})

        for champion in team['champions']:
            if 'name' in champion.keys():
                towers.append(champion['name'])

        #WAVE SORTING ALGORITHM (BASED ON UPGRADES & NUMBER OF MERCS AND RESPECTIVE DISTRIBUTION (ROUGH))
        if 'Ironback' in wave.keys():
            count += len(wave['Ironback'])
            for upgrade in wave['Ironback']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade']
        if 'Razorfin' in wave.keys():
            count += len(wave['Razorfin'])
            for upgrade in wave['Razorfin']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade']
        if 'Ocklepod' in wave.keys():
            count += len(wave['Ocklepod'])
            for upgrade in wave['Ocklepod']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade']
        if 'Plundercrab' in wave.keys():
            count += len(wave['Plundercrab'])
            for upgrade in wave['Plundercrab']:
                stats += upgrade['offense'] + upgrade['defense']
                upgrades += upgrade['upgrade']

        if count != 0:
            if upgrades/count < 0.5:
                num = math.floor(stats / 6) #1 - 5
                if num == 0:
                    num += 1
                k = "wave" + str(num)
            elif upgrades/count < 1.5:
                num = 5 + math.floor(stats / 3) #6 - 15
                if num == 0:
                    num += 1
                k = "wave" + str(num)
            elif upgrades/count < 2.5:
                num = 15 + math.floor(stats / 3) #16 - 25
                if num == 0:
                    num += 1
                k = "wave" + str(num)
            else:
                num = 25 + math.floor(stats / 6) #26 - 30
                if num == 0:
                    num += 1
                k = "wave" + str(num)
            waves.update({'wave': merc_wave})
            waves.update({'towers': towers})
            waves.update({'matchId': match['matchId']})
        if k in all_waves.keys():
            all_waves[k].append(waves)
        else:
            all_waves.update({k: [waves]})
    return json.dumps(all_waves)


def winrate_data(api, match_id):
    BMB_data = id_to_name(api.get_BMB_data(match_id))
    champion_wr = {}
    mercenary_wr = {}
    for key, value in BMB_data.items():
        mercs = []
        for item in value:
            wins = 0
            if key == 'winner':
                wins += 1

            if item == 'champions':
                for champ in value[item]:
                    champion_wr.update({champ['name']:{'wins': wins, 'games': 1}})
            elif item != 'teamId':
                mercs.append(item)
        mercenary_wr.update({mercs:{'wins': wins, 'games': 1}})

    return {'champions':champion_wr, 'mercenaries':mercenary_wr}

def match_ids(region):
    return

if __name__ == "__main__":
    main()
