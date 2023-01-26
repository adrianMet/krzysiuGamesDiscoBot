import requests
import json
from datetime import datetime, time, timedelta

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    # Python 2.x fallback
    from argparse import Namespace


def get_summoner_details_message(name):
    summoner_name = name
    api_key = 'RGAPI-eccb934a-658a-4ff9-9e91-f0e63b6e3533'
    summoner_api_url = 'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/'
    matches_api_url = 'https://europe.api.riotgames.com/lol/match/v5/matches/'

    def get_today_timestamp():
        today = datetime.today().date()
        time_00 = time.min
        today_at_00 = datetime.combine(today, time_00)

        timestamp = int(today_at_00.timestamp())
        return timestamp

    # timestamp = get_today_timestamp()
    timestamp = ''

    def get_summoner_puuid_by_name(name, api_key, summoner_api_url):
        api_url = f'{summoner_api_url}by-name/{name}?api_key={api_key}'
        respone = requests.get(api_url)
        data = respone.json()
        puuid = data['puuid']
        return puuid

    puuid = get_summoner_puuid_by_name(summoner_name, api_key, summoner_api_url)

    def get_matches_id(puuid, api_key, timestamp):
        api_url = f'{matches_api_url}by-puuid/{puuid}/ids?startTime={timestamp}&api_key={api_key}'
        response = requests.get(api_url)
        matches_ids = response.json()
        return matches_ids

    match_ids = get_matches_id(puuid, api_key, timestamp)

    def get_summ_info_by_puuid(puuid, match_data):
        data = json.loads(match_data, object_hook=lambda d: Namespace(**d))
        participants = data.info.participants
        for i in participants:
            if i.puuid == puuid:
                return i

    def get_queueid_match(match_data):
        data = json.loads(match_data, object_hook=lambda d: Namespace(**d))
        info = data.info
        return info

    def calculate_winration(win_lose_list):
        win = 0
        lose = 0
        for ele in win_lose_list:
            if ele == True:
                win += 1
            else:
                lose += 1
        if win < lose:
            return f'{win}/{lose}(win/lose) masne win ratio, musiało być fajnie'
        elif win > lose:
            return f'{win}/{lose}(win/lose) silny przywoływacz, dodatnie win ratio, może zapalić lufke w nagrodę'
        elif win == lose:
            return f'{win}/{lose}(win/lose), szału nie ma dupy nie urywa'

    def calculate_kda(kill, death, assists):
        kda = []
        i = 0
        for k, d, a in zip(kill, death, assists):
            try:
                temp_kda = (k + a) / d
            except ZeroDivisionError:
                temp_kda = k + a
            kda.append(temp_kda)
        if len(kda) < 1:
            return 'nie były grane meczyki, serce jeszcze ma szanse'
        else:
            final_kda = sum(kda) / len(kda)
            return round(final_kda, 2)

    def get_how_much_matches(matches_list):
        if len(matches_list) <= 1:
            if summoner_name == 'Psycho93PL':
                return f'dzisiaj szurson rozgrał {len(matches_list)} mecz'
            else:
                return f'dzisiaj {summoner_name} rozgrał {len(matches_list)} mecz'
        elif len(matches_list) > 1:
            if summoner_name == 'Psycho93PL':
                return f'dzisiaj szurson rozegrał {len(matches_list)} meczy'
            else:
                return f'dzisiaj {summoner_name} rozegrał {len(matches_list)} meczy'

    def get_gamemodes_played(game_modes_id):
        aram = 0
        normal = 0
        solo_duo = 0
        flex = 0
        for mode in game_modes_id:
            if mode == 450:
                aram += 1
            elif mode == 430 or mode == 400:
                normal += 1
            elif mode == 440:
                flex += 1
            elif mode == 420:
                solo_duo += 1
        if summoner_name == 'Psycho93PL':
            return f'szurson grał tryby: aram - {aram}, normal - {normal}, solo duo - {solo_duo}, flexy - {flex}'
        else:
            return f'{summoner_name} grał tryby: aram - {aram}, normal - {normal}, solo duo - {solo_duo}, flexy - {flex}'

    def get_match_data(nickname):
        summoner_name = nickname
        match_data_wins = []
        match_data_kills = []
        match_data_assists = []
        match_data_deaths = []
        queue_ids = []
        for match in match_ids:
            api_url = f'{matches_api_url}{match}/?api_key={api_key}'
            response = requests.get(api_url)
            json_object = response.json()
            data = json.dumps(json_object, indent=2)
            extracted_summ_info = get_summ_info_by_puuid(
                get_summoner_puuid_by_name(nickname, api_key, summoner_api_url), data)
            match_data_wins.append(extracted_summ_info.win)
            match_data_kills.append(extracted_summ_info.kills)
            match_data_assists.append(extracted_summ_info.assists)
            match_data_deaths.append(extracted_summ_info.deaths)
            extracted_match_info = get_queueid_match(data)
            queue_ids.append(extracted_match_info.queueId)
        return f'{get_how_much_matches(match_ids)}\n{calculate_winration(match_data_wins)}\n' \
               f'kda dla ostatnich meczy wynosi: {calculate_kda(match_data_kills, match_data_deaths, match_data_assists)}\n' \
               f'{get_gamemodes_played(queue_ids)}'

    return get_match_data(summoner_name)
