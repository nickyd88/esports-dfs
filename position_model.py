from data_cleaner import GetData, GetLECLCS, GetRecent
import numpy as np
from agg_functions import GetRawAvgs

df = GetLECLCS()

cursplit = '2020-1'
lastsplit = '2019-2'

recent = df[(df['split'].str.startswith(cursplit) | df['split'].str.startswith(lastsplit))]
recent = recent[['league', 'split', 'date', 'week', 'side', 'position', 'player', 'team', 'gamelength',
                 'result', 'k', 'd', 'a', 'teamkills', 'teamdeaths', 'cs', 'fpts']]
recent.to_csv('data/last_two_splits_LEC_LCS.csv', index=False)

df = GetRecent()

curseason = '2020-1'

df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)

print(df.head(), df.tail())

raw_avg = GetRawAvgs(df)

df['weight'] = df['iscurrent'].apply(lambda x: 1.0 if x == 1 else 0.3)


# Define a lambda function to compute the weighted mean:
wm = lambda x: np.average(x, weights=df.loc[x.index, "weight"])

# Define a dictionary with the functions to apply for a given column:
#f = {'iscurrent': ['count'], 'fpts': [{'weighted_mean' : wm}]}

# Groupby and aggregate with your dictionary:
#player = df.groupby(["player", "result"]).agg(f)



#print(player.head())


