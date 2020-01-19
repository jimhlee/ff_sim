# two functions, per and const, to handle the data
import pandas as pd
from rule_overrides import RULE_OVERRIDES
from parse_player import parser

RULES_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/raw_rules/'

def score_per(inst, score):
    numerator, denominator = score.split('|')
    num, den = float(numerator), float(denominator)
    return (inst / den) * num

def score_const(inst, score):
    return inst * score

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
    # rules['fixed_rule'] = rules['category'].apply(lambda x: fixed_rule_overrides[position].get(x, x))
    return rules

# This will reorganize the positions after parsing into a more easily usable form
def score_players_by_position(players, rules):
    players_dict = {}
    failed_rules = set()
    for player_name, weeks in players.items():
        weeks_dict = {}
        for week_num, week_events in weeks.items():
            events_dict = {}
            for rule, rule_val in week_events.items():
                # this is where rules will fail, this is where they need to be kept track of
                try:
                    events_dict[rule] = score_event(rules, rule, rule_val)
                except:
                    failed_rules.add(rule)
            weeks_dict[week_num] = events_dict
        players_dict[player_name] = weeks_dict
    return players_dict, failed_rules

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

if __name__ == '__main__':
    all_players = parser()
    output = score_all_players(all_players)