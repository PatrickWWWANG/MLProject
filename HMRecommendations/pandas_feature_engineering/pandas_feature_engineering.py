import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm import tqdm
import matplotlib.image as mpimg
from wordcloud import WordCloud, STOPWORDS
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
import category_encoders as ce

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)

plt.rcParams['axes.unicode_minus'] = False

articles_df = pd.read_csv('../articles.csv')
customers_df = pd.read_csv('../customers.csv')
transactions_df = pd.read_csv('../transactions_train.csv').sample(n=100000).reset_index(drop=True)

# Combine tables
df = transactions_df.merge(articles_df, on='article_id', how='left')
df = df.merge(customers_df, on='customer_id', how='left')

# Continuous feature
def num_add(df, f1, f2):
    df[f'{f1}_add_{f2}'] = df[f1] + df[f2]
    return df

def num_mul(df, f1, f2):
    df[f'{f1}_mul_{f2}'] = df[f1] * df[f2]
    return df

def num_div(df, f1, f2):
    df[f'{f1}_div_{f2}'] = df[f1] / (df[f2] + df[f2].mean())
    return df

def num_log(df, f):
    df[f'log_{f}'] = np.log(1 + df[f])
    return df

def num_bin(df, f, num_bins=10, bin_type='cut'):
    if bin_type == 'cut':
        df[f'{f}_bin_{num_bins}'] = pd.cut(df[f], num_bins, labels=False)
    else:
        df[f'{f}_bin_{num_bins}'] = pd.qcut(df[f], num_bins, labels=False)
    return df

df = num_bin(df, 'age', 10, bin_type='qcut')

# Discrete feature
def one_hot_enc(df, f):
    enc = OneHotEncoder()
    enc.fit(df[f].values.reshape(-1, 1))
    one_hot_array = enc.transform(df[f].values.reshape(-1, 1)).toarray()
    df[[f'{f}_one_hot_{i}' for i in range(4)]] = one_hot_array
    return df

def hash_enc(df, f_list, n_components=8):
    ce_encoder = ce.HashingEncoder(cols=f_list, n_components=n_components).fit(df)
    df = ce_encoder.transform(df)
    df.rename(columns=zip([f'col{i}' for i in range(n_components)], [f'hash_enc_{i}' for i in range(n_components)]))
    return df

def count_enc(df, f):
    map_dict = dict(zip(df[f].unique(), range(df[f].nunique())))
    df[f'label_enc_{f}'] = df[f].map(map_dict).fillna(-1).astype('int32')
    df[f'{f}_count'] = df[f].map(df[f].value_counts())
    return df

def cross_enc(df, f1, f2):
    if f'{f1}_count' not in df.columns:
        df = count_enc(df, f1)
    if f'{f2}_count' not in df.columns:
        df = count_enc(df, f2)
    df[f'{f1}_{f2}'] = df[f1].astype('str') + '_' + df[f2].astype('str')
    df = count_enc(df, f'{f1}_{f2}')
    df[f'{f1}_{f2}_count_div_{f1}_count'] = df[f'{f1}_{f2}_count'] / (df[f'{f1}_count'] + df[f'{f1}_count'].mean())
    df[f'{f1}_{f2}_count_div_{f2}_count'] = df[f'{f1}_{f2}_count'] / (df[f'{f2}_count'] + df[f'{f2}_count'].mean())
    del df[f'{f1}_{f2}']
    return df

def group_stat(df, cat_fea, num_fea):
    for stat in tqdm(['min', 'max', 'mean', 'median', 'std', 'skew']):
        df[f'{cat_fea}_{num_fea}_groupby_{stat}'] = df.groupby(cat_fea)[num_fea].transform(stat)
    return df

cate_fea_list = ['customer_id', 'article_id', 'sales_channel_id', 'product_code', 'section_no', 'postal_code']

for col in tqdm(cate_fea_list):
    df = count_enc(df, col)
    
df = cross_enc(df, 'customer_id', 'article_id')
df = cross_enc(df, 'customer_id', 'product_code')
df = cross_enc(df, 'age', 'article_id')

df = group_stat(df, 'customer_id', 'price')
df = group_stat(df, 'age', 'price')

df.info()
