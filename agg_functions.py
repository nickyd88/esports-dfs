


def GetRawAvgs(df):
    raw_avg = df.groupby(['position', 'result']).mean()[['fpts']]
    raw_avg['weight'] = 5
    return raw_avg