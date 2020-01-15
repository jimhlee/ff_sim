import json
import os

# json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')

FF_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/'
PLAYER_DIRECTORY = FF_DIRECTORY + 'raw_players/'

def parser():
    positions_dict = {}
    for weekly_folder in os.listdir(PLAYER_DIRECTORY):
        if weekly_folder == '.DS_Store':
            continue
        week_num = weekly_folder[4:]
        week_dir = os.listdir(PLAYER_DIRECTORY + weekly_folder)
        for batch in week_dir:
            with open(PLAYER_DIRECTORY + weekly_folder + '/' + batch, 'r') as f:
                raw_batch = json.load(f)
            for player_name, events in raw_batch.items():
                parsed_week = {}
                position_name = player_name.split(' ')[-1]    
                for event in events:
                    if event == 'Bye Week':
                        continue
                    stupid_list = event.split(' ')
                    try:
                        val = int(stupid_list[0])
                    except:
                        val = 0
                    rule = ' '.join(stupid_list[1:-1])
                    parsed_week[rule] = val
                if position_name not in positions_dict:
                    positions_dict[position_name] = {}
                if player_name not in positions_dict[position_name]:
                    positions_dict[position_name][player_name] = {}
                positions_dict[position_name][player_name][week_num] = parsed_week
    return positions_dict

if __name__ == "__main__":
    stuff = parser()