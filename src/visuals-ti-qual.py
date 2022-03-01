import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections
import datetime 

import nltk
from nltk.corpus import stopwords
import re
import networkx

from eda import convert_dates
import datetime 

cancel_dates = {"lucas": datetime.datetime(2021,8,24), "giselle": datetime.datetime(2021,10,23), 
                "jaemin": datetime.datetime(2021,8,24), "ryujin": datetime.datetime(2021,10,23),
                "dababy": datetime.datetime(2021,7,25), "nicki": datetime.datetime(2021,9,13), 
                "lilbaby": datetime.datetime(2021,7,25), "saweetie": datetime.datetime(2021,9,13),
                "zayn": datetime.datetime(2021,10,28), "doja": datetime.datetime(2020,5,25), 
                "harry": datetime.datetime(2021,10,28), "adele": datetime.datetime(2020,5,25)}

def splitWords(txt):
    if type(txt) == str:
        return txt.lower().split()
    else:
        return txt

def remove_url(txt):
    """
    Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).
    """

    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, roll_days):

    misinfo_dfs = convert_dates(misinfo_dfs) # convert to datetime obj
    # group by # of days canceled
    misinfo_dfs['days_cancel'] = misinfo_dfs.apply(count_days, axis=1)
    
    discrim_dfs = convert_dates(discrim_dfs) # convert to datetime obj
    # group by # of days canceled
    discrim_dfs['days_cancel'] = discrim_dfs.apply(count_days, axis=1)
    
    assualt_dfs = convert_dates(assualt_dfs) # convert to datetime obj
    # group by # of days canceled
    assualt_dfs['days_cancel'] = assualt_dfs.apply(count_days, axis=1)

    return misinfo_dfs, discrim_dfs, assualt_dfs

def count_days(row):
    '''
    helper function to count number of days since deplatform date
    '''
    cancel_date = cancel_dates[row["indiv"].lower()]

    return row["created_at"] - cancel_date

def plot_ti(out_path, df, issue):
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Plot horizontal bar graph
    df.sort_values(by='count').plot.barh(x='words',
                      y='count',
                      ax=ax,
                      color="tomato")
    ax.set_title("Common Words Found in Tweets ~" + issue)
    
    file_name = issue + "_tiFrequency.png"
    out_path = os.path.join(out_path, file_name)
    plt.savefig(out_path, bbox_inches='tight')

def word_frequency(df):
    
    stop_words = set(stopwords.words('english'))
    
    artist_names = ['doja', 'cat', 'lucas', 'giselle', 'zayn', 'malik', 'nicki', 'minaj', 'dababy']
    
    df['text'] = df['text'].apply(remove_url)
    df['text'] = df['text'].apply(splitWords)
    
    df_before = df[(df["days_cancel"] < 0)]
    df_after = df[(df["days_cancel"] > 0)]
    
    df_before = list(itertools.chain(*df_before['text']))
    df_after = list(itertools.chain(*df_after['text']))
    
    df_before = [word for word in df_before if not word in stop_words]
    df_after = [word for word in df_after if not word in stop_words]
    
    df_before = [word for word in df_before if not word in artist_names]
    df_after = [word for word in df_after if not word in artist_names]
    
    df_before = collections.Counter(df_before)
    df_after = collections.Counter(df_after)
    
    words_before = pd.DataFrame(df_before.most_common(50),
                             columns=['words', 'count'])
    
    words_after = pd.DataFrame(df_after.most_common(50),
                             columns=['words', 'count'])
    
    return words_before, words_after

def create_visuals(arg1, arg2, arg3):
    
    misinfo_dfs = pd.read_csv(arg1)
    discrim_dfs = pd.read_csv(arg2)
    assualt_dfs = pd.read_csv(arg2)

    misinfo_dfs, discrim_dfs, assualt_dfs = preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, "14d")
    
    # convert timedelta to int 
    misinfo_dfs["days_cancel"] = misinfo_dfs["days_cancel"].dt.days
    discrim_dfs["days_cancel"] = discrim_dfs["days_cancel"].dt.days
    assualt_dfs["days_cancel"] = assualt_dfs["days_cancel"].dt.days
    
    # makes sure time period is 6 months before and after cancellation date
    misinfo_dfs = misinfo_dfs[(misinfo_dfs["days_cancel"] >= -183) | (misinfo_dfs["days_cancel"] <= 183)]
    discrim_dfs = discrim_dfs[(discrim_dfs["days_cancel"] >= -183) | (discrim_dfs["days_cancel"] <= 183)]
    assualt_dfs = assualt_dfs[(assualt_dfs["days_cancel"] >= -183) | (assualt_dfs["days_cancel"] <= 183)]
    
    misinfo_before, misinfo_after = word_frequency(misinfo_dfs)
    discrim_before, discrim_after = word_frequency(discrim_dfs)
    assualt_before, assualt_after = word_frequency(assualt_dfs)
    
    plt.clf()
    plot_ti("./data/out/", misinfo_before, "Misinformation_Before")
    plt.clf()
    plot_ti("./data/out/", misinfo_after, "Misinformation_After")
    
    plt.clf()
    plot_ti("./data/out/", discrim_before, "Discrimination_Before")
    plt.clf()
    plot_ti("./data/out/", discrim_after, "Discrimination_After")

    
    plt.clf()
    plot_ti("./data/out/", assualt_before, "Assualt_Before")
    plt.clf()
    plot_ti("./data/out/", assualt_after, "Assualt_After")