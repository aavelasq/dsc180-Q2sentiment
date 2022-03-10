import os
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import collections
import datetime 

from nltk.corpus import stopwords
import re

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

def preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, roll_days, test):

    misinfo_dfs = convert_dates(misinfo_dfs) # convert to datetime obj
    # group by # of days canceled
    misinfo_dfs['days_cancel'] = misinfo_dfs.apply(lambda x: count_days(x, test), axis=1)
    
    discrim_dfs = convert_dates(discrim_dfs) # convert to datetime obj
    # group by # of days canceled
    discrim_dfs['days_cancel'] = discrim_dfs.apply(lambda x: count_days(x, test), axis=1)
    
    assualt_dfs = convert_dates(assualt_dfs) # convert to datetime obj
    # group by # of days canceled
    assualt_dfs['days_cancel'] = assualt_dfs.apply(lambda x: count_days(x, test), axis=1)

    return misinfo_dfs, discrim_dfs, assualt_dfs

def count_days(row, test):
    '''
    helper function to count number of days since deplatform date
    '''
    cancel_date = cancel_dates[row["indiv"].lower()]

    if test:
        cancel_date = datetime.datetime(2022, 2, 6)

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

def create_visuals_qual(arg1, arg2, arg3, temp_dir, out_dir, test=False):
    
    misinfo_dfs = pd.read_csv(arg1)
    discrim_dfs = pd.read_csv(arg2)
    assualt_dfs = pd.read_csv(arg3)

    misinfo_dfs, discrim_dfs, assualt_dfs = preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, "14d", test)
    
    # convert timedelta to int 
    misinfo_dfs["days_cancel"] = misinfo_dfs["days_cancel"].dt.days
    discrim_dfs["days_cancel"] = discrim_dfs["days_cancel"].dt.days
    assualt_dfs["days_cancel"] = assualt_dfs["days_cancel"].dt.days
    
    # makes sure time period is 6 months before and after cancellation date
    misinfo_dfs = misinfo_dfs[(misinfo_dfs["days_cancel"] >= -183) | (misinfo_dfs["days_cancel"] <= 183)]
    discrim_dfs = discrim_dfs[(discrim_dfs["days_cancel"] >= -183) | (discrim_dfs["days_cancel"] <= 183)]
    assualt_dfs = assualt_dfs[(assualt_dfs["days_cancel"] >= -183) | (assualt_dfs["days_cancel"] <= 183)]
    
    temp_dir =os.path.join(temp_dir,"rq1_type/")
    misinfo_before, misinfo_after = word_frequency(misinfo_dfs)
    misinfo_before.to_csv(temp_dir + "misinfo_before.csv", index=False)
    misinfo_after.to_csv(temp_dir + "misinfo_after.csv", index=False)

    discrim_before, discrim_after = word_frequency(discrim_dfs)
    discrim_before.to_csv(temp_dir + "discrim_before.csv", index=False)
    discrim_after.to_csv(temp_dir + "discrim_after.csv", index=False)

    assualt_before, assualt_after = word_frequency(assualt_dfs)
    assualt_before.to_csv(temp_dir + "assualt_before.csv", index=False)
    assualt_after.to_csv(temp_dir + "assualt_after.csv", index=False)

    # create/check folder exists   
    out_dir =os.path.join(out_dir,"rq1_type/")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    plt.clf()
    plot_ti(out_dir, misinfo_before, "Misinformation_Before")
    plt.clf()
    plot_ti(out_dir, misinfo_after, "Misinformation_After")
    
    plt.clf()
    plot_ti(out_dir, discrim_before, "Discrimination_Before")
    plt.clf()
    plot_ti(out_dir, discrim_after, "Discrimination_After")

    plt.clf()
    plot_ti(out_dir, assualt_before, "Assualt_Before")
    plt.clf()
    plot_ti(out_dir, assualt_after, "Assualt_After")