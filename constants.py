#URLS, VERSION NUMBERS, ETC

URL_RIOT_API = {
    'base': "https://{proxy}.api.pvp.net/api/lol/{region}/{url}",
    'base_static_data': "https://global.api.pvp.net/api/lol/static-data/{region}/{url}",
    'match': "v{version}/match/{match_id}",
    'champion': "v{version}/champion/",
    'item': "v{version}/item/",
    'versions': "v{version}/versions/",
    'champion_by_id': "v{version}/champion/{champion_id}",
    'champion_img': "http://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion}"
}

API_VERSIONS = {
	'match': '2.2',
    'lol_static_data': '1.2'
}

REGIONS = {
    'brazil': 'br',
    'euope_nordic_east': 'eune',
    'europe_west': 'euw',
    'korea': 'kr',
    'latin_america_north': 'lan',
    'latin_america_south': 'las',
    'north_america': 'na',
    'oceania': 'oce',
    'russia': 'rus',
    'turkey': 'tur'
}
