import pandas as pd
from data_cleaner import GetAllRecent
from position_model import CreateExpectedValueFunctionByCol
from agg_functions import GetWeightedFptAverages
from namemap import GetNameMap
from starters_reader import getStarters
import csv

df = GetAllRecent()

df['position_weight'] = 1
pos_avg_weights = GetWeightedFptAverages(df, ['position', 'league', 'result'], 'position_weight')
getEVByPlayer = CreateExpectedValueFunctionByCol('player', df)
getEVByOpTeam = CreateExpectedValueFunctionByCol('opp_team', df)

starters = getStarters()


#print(getEVByPlayer('100 Thieves', 'Middle', 0))



matchups = [
    ['LGD Gaming', 'Royal Never Give Up'],
    ['Sandbox Gaming', 'SK Telecom T1'],
    ['LNG Esports', 'Edward Gaming'],
    ['Afreeca Freecs', 'Griffin'],
    ['JD Gaming', 'Invictus Gaming']
]

team_dict = {
    'T1': 'LGD Gaming',
    'DRX': 'Royal Never Give Up',
    'ES': 'Sandbox Gaming',
    'WE': 'SK Telecom T1'
}

l_dict = {
    'ES': 'LPL',
    'WE': 'LPL',
    'T1': 'LCK',
    'DRX': 'LCK'
}

pos_dict = {
    'TOP': 'Top',
    'JNG': 'Jungle',
    'MID': 'Middle',
    'ADC': 'ADC',
    'SUP': 'Support',
    'TEAM': 'Team'
}

projections = [
    ['Player', 'Position', 'Team', 'Opponent', 'AvgIfWin', 'AvgIfLoss', 'Salary']
]
dk = pd.read_csv('data/DKSalaries.csv')
dkmap = GetNameMap('data/dknamemap.csv')

top = dk[dk['Roster Position'] == 'TOP']
jng = dk[dk['Roster Position'] == 'JNG']
mid = dk[dk['Roster Position'] == 'MID']
adc = dk[dk['Roster Position'] == 'ADC']
sup = dk[dk['Roster Position'] == 'SUP']
team = dk[dk['Roster Position'] == 'TEAM']

pos = [top, jng, mid, adc, sup, team]

print(starters)

for p in pos:
    for index, row in p.iterrows():
        playerid = row['Name + ID']
        end = playerid.find('(')-1
        try:
            player = dkmap[playerid[1:end]]
        except KeyError:
            continue
        if player not in starters:
            print(player+' not a starter')
            continue
        position = pos_dict[row['Position']]
        league = l_dict[row['TeamAbbrev']]
        avg_w = pos_avg_weights[position, 1]
        avg_l = pos_avg_weights[position, 0]
        team = team_dict[row['TeamAbbrev']]
        salary = row['Salary']

        for m in matchups:
            if team in m:
                if team == m[0]:
                    opp = m[1]
                else:
                    opp = m[0]

        try:
            win = getEVByPlayer(player, position, league, 1) + getEVByOpTeam(opp, position, league, 1) - avg_w
            loss = getEVByPlayer(player, position, league, 0) + getEVByOpTeam(opp, position, league, 0) - avg_l
        except KeyError:
            win = 'N/A'
            loss = 'N/A'

        projections.append([player, position, team, opp, win, loss, salary])



with open('test_proj.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for item in projections:
        writer.writerow(item)
