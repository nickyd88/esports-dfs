import pandas as pd
from data_cleaner import GetAllRecent
from position_model import CreateExpectedValueFunctionByCol
from agg_functions import GetWeightedFptAverages
from namemap import GetNameMap
import plotly.graph_objects as go
import plotly
from plotly.colors import n_colors
import csv
import matplotlib
import matplotlib.cm as cm
from plotly.subplots import make_subplots


df = GetAllRecent()

df['position_weight'] = 1
df['player'] = df.apply(lambda x: x.team if x.position == 'Team' else x.player, axis =1)

pos_avg_weights = GetWeightedFptAverages(df, ['position', 'league', 'result'], 'position_weight')
getEVByPlayer = CreateExpectedValueFunctionByCol('player', df)
getEVByOpTeam = CreateExpectedValueFunctionByCol('opp_team', df)

leagues = ['LPL', 'LCS', 'LCK', 'LEC']

df = df[df['league'].isin(leagues)]

avg_perf = [['Player', 'Position', 'Team', 'Points in Win', 'Points in Loss']]

players = []
for index, row in df.iterrows():
    position = row['position']
    league = row['league']
    player = row['player']
    if player in players:
        continue
    else:
        players.append(player)
        avg_w = pos_avg_weights[position, league, 1]
    avg_l = pos_avg_weights[position, league, 0]
    team = row['team']

    try:
        win = getEVByPlayer(player, position, league, 1) - avg_w    #+ getEVByOpTeam(opp, league, position, 1)
        loss = getEVByPlayer(player, position, league, 0) - avg_l  #+ getEVByOpTeam(opp, league, position, 0)
    except KeyError:
        win = 0
        loss = 0
    avg_perf.append([player, position, team, round(win, 1), round(loss, 1)])


teams = df[df['iscurrent'] == 1].groupby(['team', 'league']).mean()
avg_team_opp = [['Team', 'League', 'Top', 'Jungle', 'Middle', 'ADC', 'Support']]

positions = ['Top', 'Jungle', 'Middle', 'ADC', 'Support', 'Team']




## Team Data and Viz

for i, row in teams.iterrows():
    team = i[0]
    league = i[1]
    newrow = [team, league]
    for pos in positions:
        win = getEVByOpTeam(team, pos, league, 1)
        newrow.append(round(win, 1))

    avg_team_opp.append(newrow)


sorted_players = sorted(avg_perf[1:], key =lambda x: x[1]+x[0])

sorted_teams = sorted(avg_team_opp[1:], key= lambda x: x[1]+x[0])




plotly_team = []
for i in range(0, len(avg_team_opp[0])):
    for row in sorted_teams:
        try:
            plotly_team[i].append(row[i])
        except IndexError:
            plotly_team.append([row[i]])



norm = matplotlib.colors.Normalize(vmin=20, vmax=40, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('RdYlGn'))

colors = []
for col in plotly_team:
    temp = []
    for item in col:
        if type(item) == str:
            temp.append('rgb(239, 243, 255)')
        else:
            rgba = mapper.to_rgba(item, bytes=True)
            rgb = 'rgb('+str(rgba[0])+','+str(rgba[1])+','+str(rgba[2])+')'
            #print(mapper.to_rgba(item, bytes=True))
            temp.append(rgb)
    colors.append(temp)


fig = make_subplots(
    rows=5, cols=1,
    #shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "bar"}],
           [{"type": "bar"}],
           [{"type": "bar"}],
           [{"type": "bar"}]],
    #row_heights=[0.4, 0.15,0.15,0.15,0.15],
    shared_yaxes=True,
    row_titles=['Avg Points Given Up By Position', 'LPL', 'LCS', 'LCK', 'LEC']
)
fig.add_trace(
    go.Table(
        header=dict(values=avg_team_opp[0]),
         cells=dict(
             values= plotly_team,
             line_color= colors,
             fill_color= colors
         )
    ),
    row=1, col=1
)

for row in sorted_teams:
    avg = round((row[2] + row[3] + row[4] + row[5] + row[6])/5, 1)
    row.append(avg)

r = 2
for league in leagues:
    teams = []
    avgs = []
    for row in sorted_teams:
        if row[1] == league:
            teams.append(row[0])
            avgs.append(row[8])
    fig.add_trace(
        go.Bar(
            x=teams,
            y=avgs
        ),
    row=r, col=1
    )
    r += 1

fig.update_layout(
    title= 'Average Points Given up in Losses to Opposing Positions<br>With Team Avgs by League',
    title_font_size=24,
    height=1600
)
fig.update_yaxes(range=[20, 40])

fig.show()
#plotly.offline.plot(fig, filename ='pace/index.html', auto_open=False)




# Player Data & Viz

#avg_perf[0] is header
sorted_players = sorted(sorted_players, key= lambda x: x[2]+x[1]+x[0])

plotly_players = []
for i in range(0, len(avg_perf[0])):
    for row in sorted_players:
        try:
            plotly_players[i].append(row[i])
        except IndexError:
            plotly_players.append([row[i]])


norm = matplotlib.colors.Normalize(vmin=-5, vmax=5, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('RdYlGn'))

colors = []
for col in plotly_players:
    temp = []
    for item in col:
        if type(item) == str:
            temp.append('rgb(239, 243, 255)')
        else:
            rgba = mapper.to_rgba(item, bytes=True)
            rgb = 'rgb('+str(rgba[0])+','+str(rgba[1])+','+str(rgba[2])+')'
            #print(mapper.to_rgba(item, bytes=True))
            temp.append(rgb)
    colors.append(temp)


fig = go.Figure(data=[go.Table(
        header=dict(values=avg_perf[0][0:4]),
        cells=dict(
            values= plotly_players[0:4],
            line_color= colors[0:4],
            fill_color= colors[0:4]
         )
    )
])
fig.update_layout(
    title='Average Points In Win Above Position Average<br>Points Above Average By Position In Win',
    title_font_size=24,
    width=1000
)
fig.show()
plotly.offline.plot(fig, filename ='player_performance/index.html', auto_open=False)