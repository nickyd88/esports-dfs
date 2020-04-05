from data_cleaner import GetData, GetLECLCS, GetRecent
import numpy as np
from agg_functions import GetRawAvgsDF
import pandas as pd

df = GetRecent()

curseason = '2020-1'

df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)


raw_avg = GetRawAvgsDF(df)

df['weight'] = df['iscurrent'].apply(lambda x: 1.0 if x == 1 else 0.3)


# calculated weighted means -- confirmed via excel this function works
test = df.groupby(['player', 'position', 'result']).apply(lambda dfx: (dfx["fpts"] * dfx["weight"]).sum() / dfx["weight"].sum())
test.rename('avg_fpts')
test.to_frame()

g = df.groupby(['player','position', 'result'])
newdf = g.apply(lambda x: pd.Series([np.average(x['fpts'], weights=x['weight']),
                             np.count_nonzero(x['weight'])],
                                    index=['fpts','count'])).unstack()


print(newdf.head(10))


## STILL NEED TO ADD 5 ROWS FROM



