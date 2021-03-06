import numpy as np
import pandas as pd
import math
import pickle

# Read & clean historic data & add fantasy points
# CMD+/ MAS COMMENTS SELECTIONS
#df2017 = pd.read_csv("data/2017_all_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
#df2018a = pd.read_csv("data/2018_spring_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
#df2018b = pd.read_csv("data/2018_summer_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
#df2019a = pd.read_csv("data/2019_spring_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
#df2019b = pd.read_csv("data/2019_summer_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
# dfpre = pd.read_csv("data/df_all_pre2020.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
# df2020a = pd.read_csv("data/2020_spring_current0420.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')
#
# newcols = {
#     'kills': 'k',
#     'deaths': 'd',
#     'assists': 'a',
#     'firstblood': 'fb',
#     'dragons': 'teamdragkills',
#     'barons': 'teambaronkills',
#     'towers': 'teamtowerkills'
# }
#
# df2020a = df2020a.rename(columns=newcols)
# df2020a['position'] = df2020a['position'].apply(lambda x:
#                                                 'Team' if x == 'team' else
#                                                 'Support' if x == 'sup' else
#                                                 'ADC' if x == 'bot' else
#                                                 'Middle' if x == 'mid' else
#                                                 'Jungle' if x == 'jng' else
#                                                 'Top' if x == 'top' else 'na')
#
# df2020a['team'] = df2020a['team'].apply(lambda x:
#                                                 'JD Gaming' if x.startswith('JD Gaming') else
#                                                 'LGD Gaming' if x.startswith('LGD Gaming') else
#                                                 'SK Telecom T1' if x == 'T1' else
#                                                 x)
#
#
# df_all = pd.concat([dfpre, df2020a], sort=False)
#
# numeric_cols = [
#     'k',
#     'a',
#     'd',
#     'minionkills',
#     'monsterkills',
#     'monsterkillsownjungle',
#     'monsterkillsenemyjungle',
#     'totalgold',
#     'teamtowerkills',
#     'opptowerkills',
#     'teambaronkills',
#     'oppbaronkills',
#     'teamdragkills',
#     'oppdragkills',
#     'gamelength',
#     'date',
#     'result',
#     'fb' #first blood yes/no
# ]
#
# df_all[numeric_cols] = df_all[numeric_cols].apply(pd.to_numeric, errors='coerce')
#
# cs = []
# for index, row in df_all.iterrows():
#     cs.append(row.minionkills + row.monsterkills)
# df_all['cs'] = cs
#
# fpts = []
# for index, row in df_all.iterrows():
#     #LPL missing cs, fb, and baron data
#     if math.isnan(row.teambaronkills):
#         if row.result == 1:
#             bar = 1.25
#         else:
#             bar = 0.1
#     else:
#         bar = row.teambaronkills
#
#     if math.isnan(row.fb):
#         if row.result == 1:
#             fb = 0.75
#         else:
#             fb = 0.25
#     else:
#         fb = row.fb
#
#     if math.isnan(row.cs):
#         if row.position == 'Support':
#             cs = 50
#         elif row.position == 'Jungle':
#             cs = 250
#         else:
#             cs = 350
#     else:
#         cs = row.cs
#
#     if row.gamelength > 100:
#         leng = row.gamelength/60
#     else:
#         leng = row.gamelength
#
#     if row.position == 'sup':
#         row.position = 'Support'
#     elif row.position == 'top':
#         row.position = 'Top'
#     elif row.position == 'jng':
#         row.position = 'Jungle'
#     elif row.position == 'mid':
#         row.position = 'Middle'
#     elif row.position == 'bot':
#         row.position = 'ADC'
#     elif row.position == 'team':
#         row.position = 'Team'
#
#     if row.position == 'Team':
#         fpts.append(row.teamtowerkills + 3*bar + 2*row.teamdragkills + 2*fb + 2*row.result + 2*(1 if leng < 30 else 0))
#     else:
#         fpts.append(3*row.k + 2*row.a - 1*row.d + 0.02*cs + 2*(1 if row.k >= 10 or row.a > 10 else 0))
# df_all['fpts'] = fpts
#
# df_all.to_csv('data/df_all.csv', index=False)
#
#




def GetData():
    datatypes ={
        'gameid': str,
        'url': str,
        'league': str,
        'split': str,
        'date': float,
        'week': str,
        'game': str,
        'patchno': float,
        'playerid': 'Int64',
        'side': str,
        'position': str,
        'player': str,
        'team': str,
        'champion': str,
        'ban1': str,
        'ban2': str,
        'ban3': str,
        'ban4': str,
        'ban5': str,
        'gamelength': float,
        'result': 'Int64',
        'k': 'Int64',
        'd': 'Int64',
        'a': 'Int64',
        'teamkills': 'Int64',
        'teamdeaths': 'Int64',
        'doubles': 'Int64',
        'triples': 'Int64',
        'quadras': 'Int64',
        'pentas': 'Int64',
        'fb': 'Int64',
        'fbassist': 'Int64',
        'fbvictim': 'Int64',
        'fbtime': float,
        'kpm':  float,
        'okpm': float,
        'ckpm': float,
        'fd': 'Int64',
        'fdtime': float,
        'teamdragkills': 'Int64',
        'oppdragkills': 'Int64',
        'elementals': 'Int64',
        'oppelementals': 'Int64',
        'firedrakes':'Int64',
        'waterdrakes':'Int64',
        'earthdrakes':'Int64',
        'airdrakes':'Int64',
        'elders':'Int64',
        'oppelders':'Int64',
        'herald':'Int64',
        'heraldtime': float,
        'ft': 'Int64',
        'fttime': float,
        'firstmidouter':'Int64',
        'firsttothreetowers':'Int64',
        'teamtowerkills':'Int64',
        'opptowerkills':'Int64',
        'fbaron':'Int64',
        'fbarontime': float,
        'teambaronkills':'Int64',
        'oppbaronkills':'Int64',
        'dmgtochamps':'Int64',
        'dmgtochampsperminute':float,
        'dmgshare':float,
        'earnedgoldshare': float,
        'wards':'Int64',
        'wpm':float,
        'wardshare':float,
        'wardkills':'Int64',
        'wcpm':float,
        'visionwards':'Int64',
        'visionwardbuys':'Int64',
        'visiblewardclearrate':float,
        'invisiblewardclearrate':float,
        'totalgold':'Int64',
        'earnedgpm':float,
        'goldspent':'Int64',
        'gspd':float,
        'minionkills':'Int64',
        'monsterkills':'Int64',
        'monsterkillsownjungle':'Int64',
        'monsterkillsenemyjungle':'Int64',
        'cspm':float,
        'goldat10':'Int64',
        'oppgoldat10':'Int64',
        'gdat10':'Int64',
        'goldat15':'Int64',
        'oppgoldat15':'Int64',
        'gdat15':'Int64',
        'xpat10':'Int64',
        'oppxpat10':'Int64',
        'xpdat10':'Int64',
        'csat10':'Int64',
        'oppcsat10':'Int64',
        'csdat10':'Int64',
        'csat15':'Int64',
        'oppcsat15':'Int64',
        'csdat15':'Int64',
        'heraldkills':'Int64',
        'oppheraldkills':'Int64',
        'cs':'Int64',
        'fpts':float
    }

    return pd.read_csv("data/df_all.csv", dtype=datatypes)

def GetLECLCS():
    df_all = GetData()
    return df_all[df_all["league"].isin(['LCS', 'LEC'])]

def GetAllRecent():

    df = pd.read_csv('data/last_two_splits_all.csv')
    df['side'] = df['side'].astype(str)

    #filter for 1 row per team per game
    teams = df[df['position'] == 'Team'][['gameid', 'date', 'team', 'side']]

    # define what the opponent side was
    teams['oppside'] = np.where(teams['side'] == 'Red', 'Blue', 'Red')

    # call the team opponent team
    teams.rename(columns={'team':'opp_team'}, inplace=True)

    #drop side and rename oppside as side for joininging back on existing dataframe
    #makes join simpler and has correct column names already
    teams.drop(columns=['side'], inplace=True)
    teams.rename(columns={'oppside': 'side'}, inplace=True)

    df = pd.merge(df,
                teams,
                on=['gameid', 'date', 'side'],
                how='inner')

    return df

def GetRecentLECLCS():
    df = pd.read_csv('data/last_two_splits_LEC_LCS.csv')
    df['side'] = df['side'].astype(str)

    #filter for 1 row per team per game
    teams = df[df['position'] == 'Team'][['gameid', 'date', 'team', 'side']]

    # define what the opponent side was
    teams['oppside'] = np.where(teams['side'] == 'Red', 'Blue', 'Red')

    # call the team opponent team
    teams.rename(columns={'team':'opp_team'}, inplace=True)

    #drop side and rename oppside as side for joininging back on existing dataframe
    #makes join simpler and has correct column names already
    teams.drop(columns=['side'], inplace=True)
    teams.rename(columns={'oppside': 'side'}, inplace=True)

    df = pd.merge(df,
                teams,
                on=['gameid', 'date', 'side'],
                how='inner')

    return df

#
#
# #Load & calls a data cleaner function to clean LEC (euro) and LCS (NA) data
# df = GetLECLCS()
#
# cursplit = '2020-1'
# lastsplit = '2019-2'
#
# recent = df[(df['split'].str.startswith(cursplit) | df['split'].str.startswith(lastsplit))]
# recent = recent[['gameid', 'date', 'league', 'split', 'side', 'week', 'side', 'position', 'player', 'team', 'gamelength',
#                  'result', 'k', 'd', 'a', 'teamkills', 'teamdeaths', 'cs', 'fpts']]
# #recent.to_csv('data/last_two_splits_LEC_LCS.csv', index=False)
#
# #Load & calls a data cleaner function to clean all league data
# df = GetData()
#
# cursplit = '2020-1'
# lastsplit = '2019-2'
#
# recent = df[(df['split'].str.startswith(cursplit) | df['split'].str.startswith(lastsplit))]
# recent = recent[['gameid', 'date', 'league', 'split', 'side', 'week', 'side', 'position', 'player', 'team', 'gamelength',
#                  'result', 'k', 'd', 'a', 'teamkills', 'teamdeaths', 'cs', 'fpts']]
# recent.to_csv('data/last_two_splits_all.csv', index=False)
#
#

