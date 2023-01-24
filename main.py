import requests
import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace

summoner_name = 'Psycho93PL'
api_key = 'RGAPI-be3f4ea3-1846-4aea-8763-7d9239d42bb8'
summoner_api_url = 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/'
matches_api_url = 'https://europe.api.riotgames.com/lol/match/v5/matches/'


def get_summoner_puuid_by_name(name, api_key, summoner_api_url):
    api_url = f'{summoner_api_url}by-name/{name}?api_key={api_key}'
    respone = requests.get(api_url)
    data = respone.json()
    puuid = data['puuid']
    return puuid


puuid = get_summoner_puuid_by_name(summoner_name, api_key, summoner_api_url)


def get_matches_id(puuid, api_key):
    api_url = f'{matches_api_url}by-puuid/{puuid}/ids?start=0&count=3&api_key={api_key}'
    response = requests.get(api_url)
    matches_ids = response.json()
    return matches_ids


match_ids = get_matches_id(puuid, api_key)


def get_match_data(match_ids, api_key):
    api_url = f'{matches_api_url}{match_ids[0]}/?api_key={api_key}'
    response = requests.get(api_url)
    json_object = response.json()
    data = json.dumps(json_object, indent=3)
    return data
# def get_match_data(match_ids, api_key):
#     match_data = []
#     for ele in match_ids:
#         api_url = f'{matches_api_url}{ele}/?api_key={api_key}'
#         response = requests.get(api_url)
#         json_object = response.json()
#         match_data.append(json_object)
#     data = json.dumps(match_data, indent=3)
#     return data


match_data = get_match_data(match_ids, api_key)


def get_summ_info_by_puuid(puuid, match_data):
    data = json.loads(match_data, object_hook=lambda d: Namespace(**d))
    participants = data.info.participants
    for i in participants:
        if i.puuid == puuid:
            return i
def get_summ_metadata_by_puuid(puuid, match_data):
    data = json.loads(match_data, object_hook=lambda d: Namespace(**d))
    metadata = data.metadata.participants
    for i in metadata:
        if i == puuid:
            return data.metadata

get_my_summoner_info = get_summ_info_by_puuid(puuid, match_data)
get_my_summoner_metadata = get_summ_metadata_by_puuid(puuid, match_data)
