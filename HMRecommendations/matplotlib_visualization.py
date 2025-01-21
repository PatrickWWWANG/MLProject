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

articles = pd.read_csv('articles.csv')
customers = pd.read_csv('customers.csv')
transactions = pd.read_csv('transactions_train.csv')