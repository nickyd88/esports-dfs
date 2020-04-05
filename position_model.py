from data_cleaner import GetData, GetLECLCS, GetRecent
import numpy as np
from agg_functions import GetRawAvgsDF, GetWeightedFptAverages, GetWeightSums
import pandas as pd

df = GetRecent()

curseason = '2020-1'

df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)

raw_avg = GetRawAvgsDF(df, ['position', 'result'])

#apply weights to real games
df['season_weight'] = df['iscurrent'].apply(lambda x: 1.0 if x == 1 else 0.3)

def CreateExpectedValueFunctionByCol(col, df):
    df['position_weight'] = 1
    pos_avg_weights = GetWeightedFptAverages(df, ['position', 'result'], 'position_weight')
    grouping_avg_weights = GetWeightedFptAverages(df, [col, 'position', 'result'], 'season_weight')
    grouping_season_weight_sum = GetWeightSums(df, [col, 'position', 'result'], 'season_weight')
    print(pos_avg_weights.head(10))
    print(grouping_avg_weights.head(10))
    print(grouping_season_weight_sum.head(10))
    return lambda col_val, position, result: \
        (5 * pos_avg_weights[position,result] + \
        grouping_season_weight_sum[col_val, position,result] * grouping_avg_weights[col_val, position,result]) /\
        (5+grouping_season_weight_sum[col_val, position,result])

getEVByPlayer = CreateExpectedValueFunctionByCol('player', df)
getEVByOpTeam = CreateExpectedValueFunctionByCol('opp_team', df)


# # calculated weighted means -- confirmed via excel this function works
# newdf = GetWeightedAverages(df, ['player', 'position', 'result'], 'seas')

# print(newdf.head(10))


## STILL NEED TO ADD 5 ROWS FROM



