__author__ = "Bouhm"
#URLS, VERSION NUMBERS, ETC

URL_RIOT_API = {
    'base': "https://{proxy}.api.pvp.net/api/lol/{region}/{url}",
    'base_static_data': "https://global.api.pvp.net/api/lol/static-data/{region}/{url}",
    'match': "v{version}/match/{match_id}",
    'champion': "v{version}/champion/",
    'item': "v{version}/item",
    'versions': "v{version}/versions",
    'champion_by_id': "v{version}/champion/{champion_id}",
    'champion_img': "http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion}",
    'item_img': "http://ddragon.leagueoflegends.com/cdn/{version}/img/item/{item}"
}

API_VERSIONS = {
	'match': '2.2',
    'lol_static_data': '1.2'
}

REGIONS = [
    'br',
    'eune',
    'euw',
    'kr',
    'lan',
    'las',
    'na',
    'oce',
    'rus',
    'tur'
]
