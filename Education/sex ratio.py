import pandas as pd; import numpy as np

df = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\교육팀\\sex ratio.csv', engine='python')
years = df.columns[1:]
idx = [i for i in df.iloc[:,0] for j in years]
years = list(years) * len(df)

new_df = pd.DataFrame()
new_df['지역'] = idx; new_df['연도'] = years; new_df['성비'] = np.array(df.iloc[:,1:]).reshape(len(idx))
new_df.to_csv('C:\\Users\\myeon\\Desktop\\Data Science\\교육팀\\new sex ratio.csv', encoding = 'euc-kr')

##

df = pd.read_csv('C:\\Users\\myeon\\Desktop\\Data Science\\교육팀\\province data.csv', engine='python')
gdp = df.groupby(['id'])['gdp'].mean()
unemployment = df.groupby(['id'])['unemployment'].mean()
sexratio = df.groupby(['id'])['sexratio'].mean()

from matplotlib import pyplot as plt

plt.scatter(gdp[sexratio >= 110], unemployment[sexratio >= 110], color='blue', marker='x')
plt.scatter(gdp[sexratio < 110], unemployment[sexratio < 110], color='red', marker='^')
plt.xlabel('GDP'); plt.ylabel('UNEMPLOYMENT')
plt.show()
