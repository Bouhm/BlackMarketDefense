__author__ = 'Bouhm'
#Methods that access API and return dictionary/JSON files of data
#d

import requests
import json
import re
import pprint
from constants import URL_RIOT_API as API, API_VERSIONS as VER

class RiotAPIData(object):

    def __init__(self, api_key, region='na'):
        self.api_key = api_key
        self.region = region

    #Fetch API url and get JSON data
    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(
            API['base'].format(
                proxy = self.region,
                region = self.region,
                url = api_url
            ),
            params = args
        )
        return response.json()

    #Get all mercenaries and upgrades purchased in match
    #Return python dictionary of mercenaries and upgrades
    def _get_BMB_mercs(self):
        args = {'api_key': self.api_key, 'itemListData': 'groups'}
        api_url = API['item'].format(version=VER['lol_static_data'])
        response = requests.get(
            API['base_static_data'].format(
                proxy = self.region,
                region = self.region,
                url = api_url
            ),
            params=args
        )
        items = response.json()
        merc = {}
        merc_upgrade = []
        for item in items['data'].values():
            group = [value for key, value in item.items() if 'group' in key]
            if len(group) != 0 and 'BWMerc' in group[0]:
                if ('Upgrade' in group[0] or 'Offense' in group[0] or 'Defense' in group[0]):
                    merc_upgrade.append(item['id'])
                else:
                    merc.update({item['id']:item['name']})
        merc.update({'mercUpgrades':merc_upgrade})
        return merc

    #Get all relevant data from BMB matches
    #Return dictionary of champion ids, champion item ids, mercenaries, and respective upgrades
    def get_BMB_data(self, match_id=None, file=None):
        if file == None:
            match_data = self._request(
                API['match'].format(
                    version = VER['match'],
                    match_id = match_id
                ),
                {'includeTimeline':'true'}
            )
        else:
            match_data = file

        teams_data = self._get_teams_data(match_data)
        # if teams_data['winner']['teamId'] == '100':
        #     winner = ['1', '2', '3', '4', '5']
        # else:
        #     winner = ['6', '7', '8', '9', '10']

        player_mercs = {}
        timeline = match_data['timeline']['frames']
        for events in timeline:
            if 'events' in events.keys():
                for event in events['events']:
                    if event['eventType'] == 'ITEM_PURCHASED':
                        item_id = event['itemId']
                        participant = str(event['participantId'])
                        if item_id in [3611, 3612, 3613, 3614]: #Mercenaries
                            player_mercs.update({participant:{'merc': item_id}})
                            player_mercs[participant].update({'offense': 0, 'defense':0, 'upgrade':0})
                        elif item_id in [3621, 3622, 3623]:
                            player_mercs[participant]['offense'] += 1
                        elif item_id in [3624, 3625, 3626]:
                            player_mercs[participant]['defense'] += 1
                        elif item_id in [3615, 3616, 3617]:
                            player_mercs[participant]['upgrade'] += 1

        for player in player_mercs:
            # if player in winner:
            #     team = 'winner'
            # else:
            #     team = 'loser'
            if float(player) < 6:
                team = '100'
            else :
                team = '200'

            merc_data = player_mercs[player].copy()
            if player_mercs[player]['merc'] in teams_data[team].keys():
                del merc_data['merc']
                teams_data[team][player_mercs[player]['merc']].append(merc_data)
            else:
                del merc_data['merc']
                teams_data[team].update({player_mercs[player]['merc']:[merc_data]})
        return teams_data

    #Get data from each team from given match data dictionary
    #Return dictionary
    def _get_teams_data(self, match_data):
        winner = 0
        loser = 0
        #Exclude flasks, trinkets, wards
        item_exc = [
            '2140', '2138', '2139', '2137',
            '3340', '3341', '3342', '3361', '3362', '3363', '3364',
            '2043', '2044'
        ]
        for team in match_data['teams']:
            if team['winner'] == True:
                winner = '100'
                loser = '200'
            else:
                loser = '100'
                winner = '200'
            break

        result = {'matchId':match_data['matchId'], winner:{'winner': True, 'champions':[]}, loser:{'winner': False, 'champions': []}}
        for player in match_data['participants']:
            if str(player['teamId']) == winner:
                items = [value for key, value in player['stats'].items() if ('item' in key) and (str(value) not in item_exc)]
                result[winner]['champions'].append({'championId': player['championId'], 'items': items})
            else:
                items = [value for key, value in player['stats'].items() if ('item' in key) and (str(value) not in item_exc)]
                result[loser]['champions'].append({'championId': player['championId'], 'items': items})
        return result

    #Returns champion name string given champion id integer
    def _get_champion_by_id(self, champion_id):
        args = {'api_key': self.api_key, 'champData':'all'}
        api_url = API['champion_by_id'].format(version=VER['lol_static_data'], champion_id = champion_id)
        response = requests.get(
            API['base_static_data'].format(
                proxy = self.region,
                region = self.region,
                url = api_url
            ),
            params = args
        )
        champion_data = response.json()
        return champion_data['name']

    #Get latest static version to access Riot's static data database
    def _get_static_data_version(self):
        args = {'api_key': self.api_key}
        api = API['versions'].format(version=VER['lol_static_data'])
        response = requests.get(API['base_static_data'].format(
            proxy = self.region,
            region = self.region,
            url = api),
            params = args
        )
        versions = response.json()
        return versions[0]

    def get_all_items(self):
        args = {'api_key': self.api_key}
        api_url = API['item'].format(version=VER['lol_static_data'])
        response = requests.get(
            API['base_static_data'].format(
                proxy = self.region,
                region = self.region,
                url = api_url
            ),
            params=args
        )
        items = response.json()
        version = self._get_static_data_version()
        item_list = []
        for item in items['data'].values():
            img_url = API['item_img'].format(version=version, item=item['id']) + ".png"
            item_data = {'itemId': item['id'], 'name': item['name'], 'img': img_url}
            item_list.append(item_data)
        return json.dumps(item_list)

    #Get all champion names, IDs, and image URIs
    #Return JSON file of data
    def get_all_champs(self):
        version = self._get_static_data_version()
        args = {'api_key': self.api_key, 'champData': 'image'}
        url = API['champion'].format(version=VER['lol_static_data'])
        response = requests.get(
            API['base_static_data'].format(
                proxy = self.region,
                region = self.region,
                url = url
            ),
            params = args
        )
        champions = response.json()
        champions_data = []
        for champion in champions['data'].values():
            champ_data = {
                'name': champion['name'],
                'championId': champion['id'],
                'img': API['champion_img'].format(version=version, champion=champion['image']['full'])
            }
            champions_data.append(champ_data)
        return json.dumps(champions_data)

    # For offline testing
    def _test_sample_data(self):
        with open("sample.json") as file:
            return json.load(file)
