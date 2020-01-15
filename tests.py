import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

r = requests.get('https://www67.myfantasyleague.com/2019/options?L=57573&O=09')
soup = BeautifulSoup(r.text, 'html.parser')

raw_list = soup.find_all('table')

temp = []
for table in raw_list[1:-1]:
    player_set =  next(table.find_all('span')[0].children)
    set_name = player_set[10:-1].replace(', ','|')
    rows = table.findChildren('tr')
    raw_data = []
    for row in rows[1:]:
        cat, rng, res = (elem.text for elem in list(row.children)[0:3])
        # need to make range into min/max ints
        is_neg = rng[0] == '-'
        raw_min, raw_max = rng.split('-')[-2:]
        final_min, final_max = int(raw_min), int(raw_max)
        final_min = -final_min if is_neg else final_min
        # turn score rules into shorthand
        if 'every' in res:
            x,y = res.split(' ')[0], res.split(' ')[-1]
            func = 'per'
            func_args = f'{x}|{y}'
        elif 'each' in res:
            x = res.split(' ')[0]
            func = 'per'
            func_args = f'{x}|1'
        else:
            func = 'const' 
            func_args= res
        raw_data.append((cat, final_min, final_max, func, func_args))
    df = pd.DataFrame(raw_data, columns=['category','min','max','ref_func','ref_args'])
    df.to_csv(f'/Users/jimhlee23/learnpython/fantasy_football/raw_rules/{set_name}.csv')

# list(list(list(blah.children)[0].children)[0].children)
# THAT IS THE CAPTION FOR RULES FOR ST