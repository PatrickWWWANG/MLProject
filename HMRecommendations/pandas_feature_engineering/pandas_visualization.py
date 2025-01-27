import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm
import matplotlib.image as mpimg
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

plt.rcParams['axes.unicode_minus'] = False

articles_df = pd.read_csv('../articles.csv')
customers_df = pd.read_csv('../customers.csv')
transactions_df = pd.read_csv('../transactions_train.csv').sample(n=100000).reset_index(drop=True)

# Plot number of transactions each date
df = transactions_df.groupby(['t_dat'])['article_id'].count().reset_index()
df['t_dat'] = df['t_dat'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df.columns = ['Date', 'Transactions']
fig, ax = plt.subplots(1, 1, figsize=(16, 6))
plt.plot(df['Date'], df['Transactions'], color='Darkgreen')
plt.xlabel('Date')
plt.ylabel('Transactions')
plt.title('Transactions per Day')
plt.savefig('Transactions per Day.png')

# Plot number of transactions each date in different channel
df = transactions_df.groupby(['t_dat', 'sales_channel_id'])['article_id'].count().reset_index()
df['t_dat'] = df['t_dat'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df.columns = ['Date', 'Sales Channel ID', 'Transactions']
fig, ax = plt.subplots(1, 1, figsize=(16, 6))
g1 = ax.plot(df.loc[df['Sales Channel ID'] == 1, "Date"], df.loc[df['Sales Channel ID'] == 1, 'Transactions'], label='Sales Channel 1', color='blue')
g2 = ax.plot(df.loc[df['Sales Channel ID'] == 2, "Date"], df.loc[df['Sales Channel ID'] == 2, 'Transactions'], label='Sales Channel 2', color='pink')
plt.xlabel('Date')
plt.ylabel('Transactions')
ax.legend()
plt.title('Transactions per Day by Sales Channel')
plt.savefig('Transactions per Day by Sales Channel.png')

# Plot number of unique articles each date in different channel
df = transactions_df.groupby(['t_dat', 'sales_channel_id'])['article_id'].nunique().reset_index()
df['t_dat'] = df['t_dat'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df.columns = ['Date', 'Sales Channel ID', 'Unique Articles']
fig, ax = plt.subplots(1, 1, figsize=(16, 6))
g1 = ax.plot(df.loc[df['Sales Channel ID'] == 1, 'Date'], df.loc[df['Sales Channel ID'] == 1, 'Unique Articles'], label='Sales Channel 1', color='blue')
g2 = ax.plot(df.loc[df['Sales Channel ID'] == 2, 'Date'], df.loc[df['Sales Channel ID'] == 2, 'Unique Articles'], label='Sales Channel 2', color='pink')
plt.xlabel('Date')
plt.ylabel('Unique Articles')
ax.legend()
plt.title('Unique Articles per Day by Sales Channel')
plt.savefig('Unique Articles per Day by Sales Channel.png')
