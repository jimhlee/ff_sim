import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import json
import os
import itertools


MASTER_URL = 'https://www67.myfantasyleague.com/2019/detailed?{}&W={}&YEAR=2019'
FF_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/'
PLAYER_DIRECTORY = FF_DIRECTORY + 'raw_players/'

# this function grabs the full list of players and their url/playerID/leagueID to use later
def get_full_player_list():
    if 'player_list.json' in os.listdir(FF_DIRECTORY):
        print('player_list found. Loading from file...')
        with open(FF_DIRECTORY + 'player_list.json', 'r') as f:
            return json.load(f)
    print('player_list not found. Scraping...')
    r = requests.get('https://www67.myfantasyleague.com/2019/player_search?L=57573&NAME=+')
    soup = BeautifulSoup(r.text, 'html.parser')

    raw_list = soup.find_all('table')
    player_list = raw_list[1].find_all('tr')

    links = {}
    for player in player_list[1:]:
        url = player.a.get('href')
        l_and_p = url.split('?')[1]
        links[player.a.text] = l_and_p
    with open(FF_DIRECTORY + 'player_list.json', 'w') as f:
        json.dump(links, f)
    return links

# this dumps the parsed players into batches of 20 jsons/players
def master_pull(info, batch_size=250):
    for week in range(1,18):
        cur_week_dir = PLAYER_DIRECTORY + f'week{week}/'
        if f'week{week}' not in os.listdir(PLAYER_DIRECTORY):
            os.mkdir(cur_week_dir)
        for i, chunk in enumerate(chunked(info.items(), batch_size)):
            if i > 3:
                continue
            print(f'Processing batch {i}...')
            if f'{i}.json' in os.listdir(cur_week_dir):
                print(f'skipping {i}')
                continue
            result = process_chunk(chunk, week)
            with open(cur_week_dir+f'{i}.json', 'w') as f:
                json.dump(result,f)
    # with open(PLAYER_DIRECTORY+f'{}.json'):

# chunks stuff
def chunked(it, size):
    it = iter(it)
    while True:
        p = tuple(itertools.islice(it, size))
        if not p:
            break
        yield p

# this parses the player/week data into chunks based on position, player, week
def process_chunk(batch, week):
    all_player_dict = {}
    for player_name, l_and_p in batch:
        week_url = MASTER_URL.format(l_and_p, week)
        r = requests.get(week_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        raw_events = soup.find_all('td', class_ = 'reallysmall')
        # events per player on a given week
        events = []
        for raw_event in raw_events:
            if raw_event.text == 'Subtotal' or len(raw_event.get('class')) > 1:
                continue
            event = raw_event.text
            events.append(event)
        all_player_dict[player_name] = events
    return all_player_dict

if __name__ == "__main__":
    full_info = get_full_player_list()
    result = master_pull(full_info)

    # butts = {}
    # # below is an argument unpacking
    # for player_name, l_and_p in full_info.items():
    #     player_results = {}
    #     for week in range(1,18):
    #         print(week)
    #         if week > 2:
    #             break
    #         week_url = MASTER_URL.format(l_and_p, week)
    #         r = requests.get(week_url)
    #         soup = BeautifulSoup(r.text, 'html.parser')
    #         events = []
    #         raw_events = soup.find_all('td', class_ = 'reallysmall')

    #         for raw_event in raw_events:
    #         # raw_events[1].findChildren('td')[1].text
    #             if raw_event.text == 'Subtotal' or len(raw_event.get('class')) > 1:
    #                 continue
    #             event = raw_event.text
    #             events.append(event)

    #         player_results[week] = events
    #     butts[player_name] = player_results

# def get_player_data(url):
# r = requests.get(url)
# soup = BeautifulSoup(r.text, 'html.parser')
# raw_list = soup.find_all('table')
# blood = raw_list[1].find_all('a')
# starts from the 5th element in blood

# output = {}
# counter = 1

# blah = soup.find_all('td', class_='points')

# for row in blah:
#     if row.a is None or len(row.get('class')) > 1:
#         continue
#     output[counter] = row.a.get('href')
#     counter += 1
    # points_list = raw_list[2].find_all('td') 

# TODO: make the weekly scoring info available

# <td class="points"><a href="https://www67.myfantasyleague.com/2019/detailed?L=57573&amp;P=0630&amp;W=1&amp;YEAR=2019">9.13</a></td><td>at Buccaneers</td>



'''
V proper syntax for finding this particular kind of shit, tag then
soup.find_all('tr', class_ = 'oddtablerow')
'''