# two functions, per and const, to handle the data
import pandas as pd
from parse_player import parser

RULES_DIRECTORY = '/Users/jimhlee23/learnpython/fantasy_football/raw_rules/'

POSITION_RULES = {
    'CB': 'CB.csv',
    'DE': 'DE.csv',
    'DT': 'DT.csv',
    'S': 'S.csv',
    'QB': 'QB|RB|LB.csv',
    'RB': 'QB|RB|LB.csv',
    'LB': 'QB|RB|LB.csv',
    'WR': 'WR.csv',
    'TE': 'TE.csv',
    'ST': 'ST.csv',
    'Def': 'Def.csv',
    'Off': 'Off.csv',
}

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

FAILED_RULES = []

def score_event(df, rule, val):
    score_df = df[(df['category'] == rule) & (df['min'] <= val) & (df['max'] >=  val)]
    try:
        score_func = score_df['ref_func'].values[0]
        score_arg = score_df['ref_args'].values[0]
    except:
        print(score_df, rule, val)
        FAILED_RULES.append(rule)
        raise
        # remove the raise, keep track of how many rules are failing and use code to fix it
    return FUNC_REF[score_func](val, score_arg)

def get_parsed_rules(position):
    raw_rules = pd.read_csv(RULES_DIRECTORY + POSITION_RULES[position])
    # correct the raw rules to match
    # return finished_rules

def thing_doer(players):
    positions_dict = {}
    for position, players in players.items():
        if position not in ['QB']:
            continue
        # replace this with a function that
        position_rules = get_parsed_rules(position)
        players_dict = {}

        for player_name, weeks in players.items():

            weeks_dict = {}
            for week_num, week_events in weeks.items():

                events_dict = {}
                for rule, rule_val in week_events.items():
                    x = score_event(position_rules, rule, rule_val)

                    # rule = lookuprule
                    # if per:
                    #     x = score_per(rule_val, score)
                    # else:
                    #     x = score_const(rule_val, score)
                    events_dict[rule] = x
                weeks_dict[week_num] = events_dict
            players_dict[player_name] = weeks_dict
        positions_dict[position_name] = players_dict
    return positions_dict

if __name__ == '__main__':
    stuff = parser()
    output = thing_doer(stuff)