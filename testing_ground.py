
import pandas as pd
import numpy as np
import scipy as sci
import statsmodels.api as sm # import statsmodels


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

top = df_all[df_all['position'] == 'Top'][['fpts', 'result', 'gamelength']].dropna()
mid = df_all[df_all['position'] == 'Middle'][['fpts', 'result', 'gamelength']].dropna()
sup = df_all[df_all['position'] == 'Support'][['fpts', 'result', 'gamelength']].dropna()


sup.dropna().to_csv('data/output.csv', index = False)


X = top[['result', 'gamelength']] ## X usually means our input variables (or independent variables)
y = top['fpts'] ## Y usually means our output/dependent variable
X = sm.add_constant(X) ## let's add an intercept (beta_0) to our model

# Note the difference in argument order
model = sm.OLS(y, X).fit() ## sm.OLS(output, input)
predictions = model.predict(X)

# Print out the statistics
print(model.summary())
