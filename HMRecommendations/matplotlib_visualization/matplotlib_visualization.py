import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm
import matplotlib.image as mpimg
from wordcloud import WordCloud, STOPWORDS

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

plt.rcParams['axes.unicode_minus'] = False

articles = pd.read_csv('../articles.csv')
customers = pd.read_csv('../customers.csv')
transactions = pd.read_csv('../transactions_train.csv')

# articles.head(10)

# Articles Frequency Plot
cols = ['index_name', 'index_group_name']
fig, axs = plt.subplots(1, len(cols), figsize=(10, 4), sharex=True, sharey=True)
fig.suptitle('Articles: Some Head Frequency Count', size=20)

for idx, col in enumerate(cols):
    axs[idx].hist(articles[col], orientation='horizontal', color='orange')
    axs[idx].set_xlabel(f'Count by {col}')
    axs[idx].set_ylabel(col)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig('Articles Some Head Frequency Count.png')

# Word Cloud Plot

stopwords = set(STOPWORDS)
def save_wordcloud(data, title=None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=stopwords,
        max_words=200,
        max_font_size=40,
        scale=5,
        random_state=1
    ).generate(str(data))
    fig = plt.figure(1, figsize=(10, 10))
    plt.axis('off')
    if title:
        fig.suptitle(title, fontsize=14)
        fig.subplots_adjust(top=1.3)
    plt.imshow(wordcloud)
    plt.savefig(f'{title}.png')

save_wordcloud(articles['detail_desc'], 'Wordcloud from Detailed Description of Articles')


# customers.head()

# Customer Age Graph
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(customers['age'], color='pink', bins=70)
ax.set_xlabel('Distribution of Customers Age')
plt.savefig('Distribution of Customers Age.png')

print(customers['club_member_status'].unique())

# Club Member Status Graph
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(customers['club_member_status'].dropna(), color='purple')
ax.set_xlabel('Distribution of Club Member Status')
plt.savefig('Distribution of Club Member Status.png')

# Fashion News Frequency Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(customers['fashion_news_frequency'].dropna(), color='lightblue')
ax.set_xlabel('Distribution of Fashion News Frequency')
plt.savefig('Distribution of Fashion News Frequency.png')


# transactions.head()

# Graph of Price Distribution on Different Channels
data1 = np.log(transactions.loc[transactions['sales_channel_id'] == 1].price.value_counts())
data2 = np.log(transactions.loc[transactions['sales_channel_id'] == 2].price.value_counts())
data3 = np.log(transactions.price.value_counts())

fig, axs = plt.subplots(3, 1, figsize=(14, 14))

# Channel 1
axs[0].hist(data1, bins=30, alpha=0.5, color='blue')
axs[0].set_title('Sales Channel 1')

# Channel 2
axs[1].hist(data2, bins=30, alpha=0.5, color='green')
axs[1].set_title('Sales Channel 2')

# All Channels
axs[2].hist(data3, bins=30, alpha=0.5, color='red')
axs[2].set_title('All Sales Channels')

plt.tight_layout()
plt.savefig('Price Distribution on Sales Channels.png')


# Table Combine

# Graph of Average Price by Time

articles_for_merge = articles[['article_id', 'prod_name', 'product_type_name', 'product_group_name', 'index_name']]
articles_for_merge = transactions[['customer_id', 'article_id', 'price', 't_dat']].merge(articles_for_merge, on='article_id', how='left')
articles_for_merge['t_dat'] = pd.to_datetime(articles_for_merge['t_dat'])

product_list = ['Shoes', 'Garment Full body', 'Bags', 'Garment Lower body', 'Underwear/nightwear']
colors = ['cadetblue', 'orange', 'mediumspringgreen', 'tomato', 'lightseagreen']
k = 0
f, ax = plt.subplots(3, 2, figsize=(20, 15))
for i in range(3):
    for j in range(2):
        try:
            product = product_list[k]
            articles_for_merge_product = articles_for_merge[articles_for_merge.product_group_name == product_list[k]]
            series_mean = articles_for_merge_product[['t_dat', 'price']].groupby(pd.Grouper(key='t_dat', freq='M')).mean().fillna(0)
            series_std = articles_for_merge_product[['t_dat', 'price']].groupby(pd.Grouper(key='t_dat', freq='M')).std().fillna(0)
            ax[i, j].plot(series_mean, linewidth=4, color=colors[k])
            ax[i, j].fill_between(series_mean.index, (series_mean.values - 2 * series_std.values).ravel(), 
                                  (series_mean.values + 2 * series_std.values).ravel(), color=colors[k], alpha=0.1)
            ax[i, j].set_title(f'Mean {product_list[k]} Price in Time')
            ax[i, j].set_xlabel('Month')
            ax[i, j].set_ylabel('Price')
            k += 1
        except IndexError:
            ax[i, j].set_visible(False)
plt.savefig('Average Price by Time.png')


# Plot Image

article_list = ['0118458004', '0108775015', '0146706005']
fig, ax = plt.subplots(1, len(article_list), figsize=(20, 10))

for i, article_id in enumerate(article_list):
    img = mpimg.imread(f'{article_id}.jpg')
    ax[i].imshow(img)
    ax[i].set_xlabel(f'{article_id}.jpg')
    ax[i].set_xticks([], [])
    ax[i].set_yticks([], [])
    ax[i].grid(False)
plt.savefig('Plot Image.png')