# File that gets data from API and does everything
import requests
import json
from constants import URL_RIOT_API as API, API_VERSIONS as VER, REGIONS as REG

class RiotAPIData(object):

    def __init__(self, api_key, region=REG['north_america']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, params={}):
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        response = requests.get(API['base'].format(proxy=self.region, region=self.region, url=api_url), params=args)
        return response.json()

    def _get_BMB_items_data(self, match_id):
        match_data = self._request(API['match'].format(version=VER['match'], match_id=match_id), {'includeTimeline':'true'})
        BMB_items = self._get_BMB_item_ids()
        teams_data = self._get_teams_data(match_data)
        timeline = match_data['timeline']['frames']
        for event in timeline:
            if (event['eventType'] == 'ITEM_PURCHASED') and (event['itemId'] in BMB_items):
                if event['participantId'] < 6:
                    teams_data['winner'].update({'mercenaries': event['itemId']})
                else:
                    teams_data['loser'].update({'mercenaries': event['itemId']})

        return teams_data

    def _get_teams_data(self, match_data):
        winner = 0
        loser = 0
        for team in match_data['teams']:
            if team['winner'] == 'true':
                winner = team['teamId']
            else:
                loser = team['teamId']

        result = {'winner':{'teamId': winner, 'champions':[]}, 'loser':{'teamId': loser, 'champions': []}}
        for player in match_data['participants']:
            champion = player['championId']
            if player['teamId'] == winner:
                for item in player['stats']:
                    items = [value for key, value in item.items() if 'item' in key]
                result['winner']['champions'].append({'championId': player['championId'], 'items': items})

            else:
                for item in player['stats']:
                    items = [value for key, value in item.items() if 'item' in key]
                result['loser']['champions'].append({'championId': player['championId'], 'items': items})

        return result

    def _get_BMB_item_ids(self):
        args = {'api_key': self.api_key, 'item':''}
        api_url = API['item'].format(version=VER['lol_static_data'])
        response = requests.get(API['base_static_data'].format(proxy=self.region, region=self.region, url=api_url), params=args)
        items = response.json()
        return

    #Returns champion name string given champion id integer
    def _get_champion_by_id(self, champion_id):
        args = {'api_key': self.api_key, 'champData':'all'}
        api_url = API['champion_by_id'].format(version=VER['lol_static_data'], champion_id=champion_id)
        response = requests.get(API['base_static_data'].format(proxy=self.region, region=self.region, url=api_url), params=args)
        champion_data = response.json()
        return champion_data['name']

    def get_all_champs(self):
        vers_args = {'api_key': self.api_key, 'versions':''}
        vers_api = API['versions'].format(version=VER['lol_static_data'])
        vers_response = requests.get(API['base_static_data'].format(proxy=self.region, region=self.region, url=vers_api), params=vers_args)
        versions = vers_response.json()
        version = versions[0]
        champ_args = {'api_key': self.api_key, 'champData':'altimages'}
        champ_url = API['champion'].format(version=VER['lol_static_data'])
        champ_response = requests.get(API['base_static_data'].format(proxy=self.region, region=self.region, url=champ_url), params=champ_args)
        champions = champ_response.json()
        champions_data = []
        for champion in champions['data'].values():
            champ_data = {
                'name': champion['name'],
                'championId': champion['id'],
                'championImg': champion['name'] + '.png'
            }
            champions_data.append(champ_data)

        return champions_data
