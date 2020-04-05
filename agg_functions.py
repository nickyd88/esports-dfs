import pandas as pd
import numpy as np

def GetRawAvgsDF(df, grouping):
    raw_avg = df.groupby(grouping).mean()[['fpts']]
    return raw_avg

def GetWeightedFptAverages(df, grouping, weight_col):
    return df.groupby(grouping).apply(wavg, 'fpts', weight_col)

def GetWeightSums(df, grouping, weight_col):
    return df.groupby(grouping).apply(wsum, weight_col)

def wsum(group, weight_col):
    w = group[weight_col]
    return w.sum()

def wavg(group, avg_col, weight_col):
    d = group[avg_col]
    w = group[weight_col]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return d.mean()