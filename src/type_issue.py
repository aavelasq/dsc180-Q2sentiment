import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import nltk
from nltk.corpus import stopwords
import re
import networkx

import datetime

cancel_dates = {"lucas": datetime.datetime(2021,8,24), "giselle": datetime.datetime(2021,10,23), 
                "jaemin": datetime.datetime(2021,8,24), "ryujin": datetime.datetime(2021,10,23),
                "dababy": datetime.datetime(2021,7,25), "nicki": datetime.datetime(2021,9,13), 
                "lilbaby": datetime.datetime(2021,7,25), "saweetie": datetime.datetime(2021,9,13),
                "zayn": datetime.datetime(2021,10,28), "doja": datetime.datetime(2020,5,25), 
                "harry": datetime.datetime(2021,10,28), "adele": datetime.datetime(2020,5,25)}


def clean_toxic_df(df):
    '''
    removes all rows where metric == 1000
    as these are tweets not recognized by the API 
    '''

    inital_df = df[df['toxicity'] != 1000] 
    inital_df = inital_df[inital_df['severe_toxicity'] != 1000]
    inital_df = inital_df[inital_df['insult'] != 1000]
    inital_df = inital_df[inital_df['profanity'] != 1000]
    
    return inital_df
    
def convert_dates(data):
    '''
    converts dates to datetime object
    '''
    # convert to datetime object
    data['created_at'] = pd.to_datetime(data['created_at']) 
    # don't localize time
    data['created_at'] = data['created_at'].dt.tz_localize(None) 

    # reset hour, min, sec to 0
    data['created_at'] = data['created_at'].apply(
        lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))
    
    return data

def group_artists_issue():
    
    discrimination = ['doja', 'dababy', 'giselle']
    misinformation = ['nicki']
    assualt = ["zayn", "lucas"]

    return discrimination, assualt, misinformation

def create_issue_df(out_dir, tweet_list, data_list):
    # out_dir, tweet_list,
    # initialize variables
    misinfo_dfs = []
    discrim_dfs = []
    assualt_dfs = []
    
    discrimination, assualt, misinformation = group_artists_issue()
    
    for data_dict in data_list:
        artist_names = list(data_dict.keys())
        
        for indiv in artist_names:
            artist_name = indiv.lower()

            toxicity_data = data_dict[indiv][0]
            cancel_date = data_dict[indiv][2]
            
            toxic_df = clean_toxic_df(toxicity_data) # remove invalid values
            toxic_df = convert_dates(toxic_df) # convert to datetime obj

        # group by how many days away from cancel date
        # toxic_df = toxic_df.groupby(["created_at"]).mean().reset_index()
            toxic_df['indiv'] = artist_name
        
            
            if artist_name in discrimination:
                discrim_dfs.append(toxic_df)
            elif artist_name in assualt:
                assualt_dfs.append(toxic_df)
            elif artist_name in misinformation:
                misinfo_dfs.append(toxic_df)

    final_misinfo = pd.concat(misinfo_dfs)
    final_misinfo.to_csv(out_dir + "misinfo_ti.csv", index=False)
    
    final_discrim = pd.concat(discrim_dfs)
    final_discrim.to_csv(out_dir + "discrim_ti.csv", index=False)
    
    final_assualt = pd.concat(assualt_dfs)
    final_assualt.to_csv(out_dir + "assualt_ti.csv", index=False)
