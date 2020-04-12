from data_cleaner import GetAllRecent
import plotly.express as px
import plotly.graph_objects as go
import plotly

df = GetAllRecent()
winners = df[df['result'] == 1].copy()

leagues = ['LPL', 'LCS', 'LCK', 'LEC']

winners = winners[winners['league'].isin(leagues)]

winners = winners.groupby(['league', 'position'])[['fpts']].mean()
winners.reset_index(inplace=True)
print(winners.head())

test = df[df['fpts'].isnull()]
print(test.head(20))
# Here we use a column with categorical data


fig = px.bar(winners, x="position", y="fpts", color='league', barmode='group',
             height=400)

fig.update_layout(
    title_text="Average Points of Winning Teams by League & Position - Last 2 Splits",
    title_font_size=18,
    xaxis_title="Position (on winning team)",
    yaxis_title='Average Points',
    width=1000,
    height=600
)

fig.show()


plotly.offline.plot(fig, filename ='avg_winners/index.html', auto_open=False)

