
import pandas as pd
import numpy as np
import scipy as sci
import statsmodels.api as sm # import statsmodels
import pickle
from data_cleaner import GetRecentLECLCS

df_all = GetRecentLECLCS()

print(df_all[['player', 'team', 'opp_team']].head(20))


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
