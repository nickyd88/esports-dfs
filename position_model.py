from data_cleaner import GetData, GetLECLCS, GetRecent



df = GetLECLCS()

cursplit = '2020-1'
lastsplit = '2019-2'

recent = df[(df['split'].str.startswith(cursplit) | df['split'].str.startswith(lastsplit))]
recent = recent[['league', 'split', 'date', 'week', 'side', 'position', 'player', 'team', 'gamelength',
                 'result', 'k', 'd', 'a', 'teamkills', 'teamdeaths', 'cs', 'fpts']]
recent.to_csv('data/last_two_splits_LEC_LCS.csv', index=False)

df = GetRecent()

print(df.dtypes)

curseason = '2020-1'

df['iscurrent'] = df['split'].apply(lambda x: 1 if x.startswith(curseason) else 0)

print(df.head())
