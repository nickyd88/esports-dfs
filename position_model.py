from data_cleaner import GetData, GetLECLCS, GetRecentLECLCS, GetAllRecent
import numpy as np
from agg_functions import GetRawAvgsDF, GetWeightedFptAverages, GetWeightSums
import pandas as pd



def CreateExpectedValueFunctionByCol(col, df):

    averageWeightVal = 2.5 # should be 5 except we're looking @ wins & losses separately

    # This is hardcoded for now in here
    curseason = '2020-1'
    df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)
    df['season_weight'] = df['iscurrent'].apply(lambda x: 1.0 if x == 1 else 0.3)

    df['position_weight'] = 1
    pos_avg_weights = GetWeightedFptAverages(df, ['position', 'result'], 'position_weight')
    grouping_avg_weights = GetWeightedFptAverages(df, [col, 'position', 'result'], 'season_weight')
    grouping_season_weight_sum = GetWeightSums(df, [col, 'position', 'result'], 'season_weight')
    #print(pos_avg_weights.head(10))
    #print(grouping_avg_weights.head(10))
    #print(grouping_season_weight_sum.head(10))
    return lambda col_val, position, result: \
        (averageWeightVal * pos_avg_weights[position,result] + \
        grouping_season_weight_sum[col_val, position,result] * grouping_avg_weights[col_val, position,result]) /\
        (averageWeightVal+grouping_season_weight_sum[col_val, position,result])



#df = GetAllRecent()

#getEVByPlayer = CreateExpectedValueFunctionByCol('player', df)
#getEVByOpTeam = CreateExpectedValueFunctionByCol('opp_team', df)

#print(getEVByOpTeam('100 Thieves', 'Middle', 0))


# # calculated weighted means -- confirmed via excel this function works
# newdf = GetWeightedAverages(df, ['player', 'position', 'result'], 'seas')

# print(newdf.head(10))


## STILL NEED TO ADD 5 ROWS FROM



