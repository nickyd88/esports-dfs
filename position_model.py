from data_cleaner import GetData, GetLECLCS, GetRecent
import numpy as np
from agg_functions import GetRawAvgsDF

df = GetRecent()

curseason = '2020-1'

df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)

print(df.head(), df.tail())

raw_avg = GetRawAvgsDF(df)

df['weight'] = df['iscurrent'].apply(lambda x: 1.0 if x == 1 else 0.3)


# calculated weighted means -- confirmed via excel this function works
test = df.groupby(['player', 'result']).apply(lambda dfx: (dfx["fpts"] * dfx["weight"]).sum() / dfx["weight"].sum())

## STILL NEED TO ADD 5 ROWS FROM

print(test.head())



