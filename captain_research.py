from data_cleaner import GetAllRecent
import plotly.express as px
import plotly.graph_objects as go
import plotly

df = GetAllRecent()
winners = df[df['result'] == 1].copy()
winners["rank"] = winners.groupby("gameid")["fpts"].rank("dense", ascending=False)

top = winners[winners['rank'] == 1].copy()

leagues = ['LPL', 'LCS', 'LCK', 'LEC']

# Here we use a column with categorical data
fig = go.Figure()

for league in leagues:
    temp = top[top['league'] == league]

    fig.add_trace(go.Histogram(
        x=temp['position'],
        histnorm='percent',
        name=league, # name used in legend and hover labels
        opacity=0.75
    ))

fig.update_layout(
    title_text="Top Scoring Position Among Winning Teams - Last 2 Splits",
    title_font_size=18,
    xaxis_title="Position of Top Scorer (DK)",
    yaxis_title='Frequency (%)',
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.05, # gap between bars of the same location coordinates
    width=1000,
    height=600
)

fig.show()


plotly.offline.plot(fig, filename ='top_scorers/index.html', auto_open=False)

