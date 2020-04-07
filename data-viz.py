
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly


df2017 = pd.read_csv("data/2017_all_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df2018a = pd.read_csv("data/2018_spring_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df2018b = pd.read_csv("data/2018_summer_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df2019a = pd.read_csv("data/2019_spring_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df2019b = pd.read_csv("data/2019_summer_final.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df2020a = pd.read_csv("data/2020_spring_current0319.csv", sep=',', error_bad_lines=False, index_col=False, dtype='unicode')

df_all = pd.concat([df2017, df2018a, df2018b, df2019a, df2019b, df2020a], sort=False)

numeric_cols = [
    'k',
    'a',
    'd',
    'minionkills',
    'monsterkills',
    'monsterkillsownjungle',
    'monsterkillsenemyjungle',
    'totalgold',
    'teamtowerkills',
    'opptowerkills',
    'teambaronkills',
    'oppbaronkills',
    'teamdragkills',
    'oppdragkills',
    'gamelength',
    'date',
    'result',
    'fb' #first blood yes/no
]

df_all[numeric_cols] = df_all[numeric_cols].apply(pd.to_numeric, errors='coerce')

cs = []
for index, row in df_all.iterrows():
    cs.append(row.minionkills + row.monsterkills + row.monsterkillsownjungle + row.monsterkillsenemyjungle)
df_all['cs'] = cs

fpts = []
for index, row in df_all.iterrows():
    if row.position == 'Team':
        fpts.append(row.teamtowerkills + 3*row.teambaronkills + 2*row.teamdragkills + 2*row.fb + 2*row.result + 2*(1 if row.gamelength < 30 else 0))
    else:
        fpts.append(3*row.k + 2*row.a - 1*row.d + 0.02*row.cs + 2*(1 if row.k >= 10 or row.a > 10 else 0))
df_all['fpts'] = fpts

pos = df_all.groupby(['position', 'result']).mean()[['k', 'd', 'a', 'cs', 'fpts']]

print(pos)
fig_df = df_all[['gamelength', 'position', 'fpts', 'result', 'player']].dropna()
fig_df['Result'] = fig_df['result'].apply(lambda x: 'Win' if x == 1 else 'Loss')
print(fig_df.head())

colorsIdx = {'Win': 'rgb(50, 168, 82)', 'Loss': 'rgb(245, 88, 104)'}
colors = fig_df['Result'].map(colorsIdx)

fig = px.scatter(
    fig_df,
    x="gamelength",
    y="fpts",
    labels=dict(
        gamelength="Game Length",
        fpts = "Fantasy Points (DK)"
    ),
    color="Result",
    color_discrete_map=colorsIdx,
    facet_col="position",
    facet_col_wrap=2,
    trendline="ols"
)
fig.update_traces(
    marker= dict(
        opacity = 0.2
    )
)

fig.update_layout(
    title_text="Fantasy Points vs. Game Length by Position & Result",
    title_font_size=24,
    xaxis_title="Game Length",
    yaxis_title='Fantasy Points (DK)',
)

fig.show()

plotly.offline.plot(fig, filename ='web_point_distributions/index.html', auto_open=False)




