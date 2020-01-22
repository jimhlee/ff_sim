import pandas as pd
import numpy as np
from rule_overrides import RULE_OVERRIDES
from parse_player import parser

RULES_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/raw_rules/'
TEST_RULES_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/test_rules/'

def score_per(inst, score):
    numerator, denominator = score.split('|')
    num, den = float(numerator), float(denominator)
    return (inst / den) * num

def score_const(inst, score):
    return float(score)

FUNC_REF = {
    'per': score_per,
    'const': score_const,
}

def score_event(df, rule, val):
    score_df = df[(df['fixed_rule'] == rule) & (df['min'] <= val) & (df['max'] >=  val)]
    score_func = score_df['ref_func'].values[0]
    score_arg = score_df['ref_args'].values[0]
    return FUNC_REF[score_func](val, score_arg)

# This will reform the irregularities in the rules and return them
def get_parsed_rules(position):
    
    rules = pd.read_csv(RULES_DIRECTORY + f'{position}.csv')
    # I'm an idiot, wrote the dict backwards so I had to flip it
    fixed_rule_overrides = {v: k for k, v in RULE_OVERRIDES[position].items()}
    rules['fixed_rule'] = rules['category'].apply(lambda x: fixed_rule_overrides.get(x, x))
    return rules

# This will reorganize the positions after parsing into a more easily usable form
def score_players_by_position(players, rules):
    players_dict = {}
    failed_rules = set()
    for player_name, weeks in players.items():
        weeks_dict = {}
        for week_num, week_events in weeks.items():
            events_dict = {}
            for rule, rule_val in week_events:
                try:
                    events_dict[rule] = score_event(rules, rule, rule_val)
                except:
                    failed_rules.add(rule)
            weeks_dict[week_num] = events_dict
        players_dict[player_name] = weeks_dict
    return players_dict, failed_rules

def get_test_rules(csv_name, position):
    rules = pd.read_csv(TEST_RULES_DIRECTORY + csv_name)
    # I'm an idiot, wrote the dict backwards so I had to flip it
    fixed_rule_overrides = {v: k for k, v in RULE_OVERRIDES[position].items()}
    rules['fixed_rule'] = rules['category'].apply(lambda x: fixed_rule_overrides.get(x, x))
    return rules

def test_scores(all_players, csv_name, position, output_name):
    '''
    This function takes custom rules for a given position set and returns the scores for all players at that position as well as any failed rules for double checking

    Args
        all_players {dict} - the master dict of all positions and all players/events for the season for each player
        csv_name {str} - The name of the custom set of rules in the test rules directory
        position {str} - The position to evaluate
        output_name {str} - The str name of the output csv in blah director 
    Returns {tuple}
        The first part of the tuple is a dict of players and their custom scores. The second part is a set of failed rules to make sure the players were successfully stored.
    '''
    players = all_players[position]
    rules = get_test_rules(csv_name, position)
    return score_players_by_position(players, rules)


# This is the main function, other functions will feed into it
def score_all_players(all_players):
    output_dict = {}
    for position, players in all_players.items():
        try:
            rules = get_parsed_rules(position)
        except FileNotFoundError:
            continue
        player_results, failed_rules = score_players_by_position(players, rules)
        output_dict[position] = {'player_results': player_results, 'baddies': failed_rules}
    return output_dict

def quick_reformat(raw_players, rules):
    unique_rules = rules['fixed_rule'].unique()
    arr = np.zeros((len(raw_players), len(unique_rules) + 1), dtype=float)
    for play_num, (player, player_stuff) in enumerate(raw_players.items()):
        for week, week_stuff in player_stuff.items():
            arr[play_num, 0] = week
            for i, rule in enumerate(unique_rules):
                arr[play_num, i+1] = week_stuff.get(rule)
    return pd.DataFrame(arr, index=list(raw_players.keys()), columns=(['week'] + list(unique_rules)))

if __name__ == '__main__':
    all_players = parser()
    rules = get_test_rules('Test_Off_3rddown.csv', 'Off')
    output = test_scores(all_players, 'Test_Off_3rddown.csv', 'Off', 'Off_results.csv')

    # output = score_all_players(all_players)