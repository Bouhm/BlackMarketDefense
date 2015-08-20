__author__ = 'Bouhm'
# File that gets data from API and does everything
import requests
import json
import re
import pprint
from constants import URL_RIOT_API as API, API_VERSIONS as VER

class RiotAPIData(object):

    def __init__(self, api_key, region='na'):
        self.api_key = api_key
        self.region = region

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

    def _get_BMB_items_data(self, match_id):
        match_data = self._request(
            API['match'].format(
                version = VER['match'],
                match_id = match_id
            ),
            {'includeTimeline':'true'}
        )

        BMB_mercs = self._get_BMB_mercs()
        teams_data = self._get_teams_data(match_data)
        if teams_data['winner']['teamId'] == '100':
            winner = ['1', '2', '3', '4', '5']
        else:
            winner = ['6', '7', '8', '9', '10']
        player_mercs = {}
        timeline = match_data['timeline']['frames']
        for events in timeline:
            if 'events' in events.keys():
                for event in events['events']:
                    if event['eventType'] == 'ITEM_PURCHASED':
                        item_id = event['itemId']
                        participant = str(event['participantId'])
                        if item_id in [3611, 3612, 3613, 3614]: #Mercenaries
                            player_mercs.update({participant:{'merc': BMB_mercs[item_id].lower()}})
                        elif item_id in [3621, 3624, 3615]: #First upgradess
                            if item_id == 3621:
                                player_mercs[participant].update({'offense': 1})
                            elif item_id == 3624:
                                player_mercs[participant].update({'defense': 1})
                            elif item_id == 3615:
                                player_mercs[participant].update({'upgrade': 1})
                        elif item_id in [3622, 3623]:

                            player_mercs[participant]['offense'] += 1
                        elif item_id in [3625, 3626]:
                            player_mercs[participant]['defense'] += 1
                        elif item_id in [3616, 3617]:
                            player_mercs[participant]['upgrade'] += 1

        for player in player_mercs:
            if player in winner:
                team = 'winner'
            else:
                team = 'loser'

            merc_data = player_mercs[player].copy()
            if player_mercs[player]['merc'] in teams_data[team].keys():
                del merc_data['merc']
                teams_data[team][player_mercs[player]['merc']].append(merc_data)
            else:
                del merc_data['merc']
                teams_data[team].update({player_mercs[player]['merc']:[merc_data]})
        return teams_data


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

        result = {'winner':{'teamId': winner, 'champions':[]}, 'loser':{'teamId': loser, 'champions': []}}
        for player in match_data['participants']:
            if str(player['teamId']) == winner:
                items = [value for key, value in player['stats'].items() if ('item' in key) and (str(value) not in item_exc)]
                result['winner']['champions'].append({'championId': player['championId'], 'items': items})
            else:
                items = [value for key, value in player['stats'].items() if ('item' in key) and (str(value) not in item_exc)]
                result['loser']['champions'].append({'championId': player['championId'], 'items': items})
        return result

    def _id_to_name(self, dict):
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
