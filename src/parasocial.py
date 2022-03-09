import pandas as pd
import os
import ast
from eda import convert_dates
from preprocessing import clean_toxic_df

engagement_threshold = 25000
fandom_threshold = 0.05
cancelled_indivs = ["lucas", "giselle", "dababy", "nicki", "zayn", "doja"]
fandom_names = {"lucas": ["nctzen", "nctzens", "wayzennie", "wayzennies", 
                        "wayzenni", "weishennie", "czennie", "czennies", "#nctzen", "#weishennie", 
                        "#nctzens", "#weishennies", "lumi", "lumis"], 
                "jaemin": ["nctzen", "nctzens", "czennie", "czennies", "#nctzen", "#nctzens", 
                        "nanadoongie", "nanadoongies"], 
                "giselle": ["MY", "MYs", "#MYs", "aerishine", "aerishines"], 
                "ryujin": ["midzy", "midzys", "#midzy"], 
                "nicki": ["barb", "barbz", "barbs", "#barbz", "#barb"], 
                "zayn": ["directioners", "directioner", "zquad", "#zquad"], 
                "harry": ["directioners", "directioner", "harries", "#harries"], 
                "adele": ["daydreamer", "daydreamers", "#daydreamer"],
                "doja": ["kittenz", "#kittenz"]}

def create_before_cancel_df(data_list):
    '''
    combines all date into one dataframe in which for each individual,
    only tweets that have been published before the individual's cancel date
    is included
    '''
    df_list = []

    for data_dict in data_list:
        artist_names = list(data_dict.keys())

        for indiv in artist_names:
            artist_name = indiv.lower()
            df = data_dict[indiv][0]
            cancel_date = data_dict[indiv][1]

            df = convert_dates(df)
            # add column to indicate which individual each value belongs to
            df["indiv"] = artist_name
            # set to subset of data before cancellation date only if cancelled
            if artist_name in cancelled_indivs:
                df = df[df["created_at"] < cancel_date]

            df_list.append(df)
    
    final_df = pd.concat(df_list).reset_index(drop=True)

    return final_df

def calc_engage_metric(df): 
    '''
    calculates engagement ratio based on input dataframe containing all artists
    '''
    temp_df = df.copy()

    # creates seperate columns from retweet, reply, like, and quote data
    temp_df['retweet_count'] = df['public_metrics'].apply(lambda x: ast.literal_eval(x)['retweet_count'])
    temp_df['reply_count'] = df['public_metrics'].apply(lambda x: ast.literal_eval(x)['reply_count'])
    temp_df['like_count'] = df['public_metrics'].apply(lambda x: ast.literal_eval(x)['like_count'])
    temp_df['quote_count'] = df['public_metrics'].apply(lambda x: ast.literal_eval(x)['quote_count'])
    # drop unneeded columns
    temp_df = temp_df.drop(columns=["public_metrics", "id", "author_id"])

    # counts tweets per individual
    final_df = temp_df.copy().groupby("indiv").count().reset_index()[['indiv']]
    final_df["num_tweets"] = temp_df.groupby("indiv").count().reset_index()['text']
    
    # calculates total mean engagement
    engage_num = (temp_df.groupby(by="indiv").mean().reset_index()['retweet_count'] + temp_df.groupby(
        by="indiv").mean().reset_index()['like_count'] + temp_df.groupby(
        by="indiv").mean().reset_index()['reply_count'] + temp_df.groupby(
        by="indiv").mean().reset_index()['quote_count'])
    final_df["num_engage"] = engage_num

    # calculates engagement ratio (total mean engagement)
    final_df["engage_ratio"] = final_df["num_engage"]
    final_df = final_df.sort_values(by="engage_ratio", ascending=False).reset_index(drop=True)
    
    return final_df

def fandom_stre_helper(df, fandom, case_sensitive=False):
    '''
    helper function for calc_fandom_strength to apply on df 
    sums the number of 1's in the df aka the number of tweets 
    that contain a fandom name
    '''
    if case_sensitive == False:
        df["num_boo"] = df['text'].apply(lambda x: 1 if fandom.lower() in x.lower() else 0)
    else:
        df["num_boo"] = df['text'].apply(lambda x: 1 if fandom in x else 0)
    
    return df["num_boo"].sum()

def calc_fandom_strength(df, fandom_list, case_sensitive=False):
    '''
    main function to calculate fandom strength by summing all instances
    of tweets that contain some variation of an artist's fandom name 
    '''
    final_sum = 0
    if case_sensitive == False:
        for fandom in fandom_list: 
            init_sum = fandom_stre_helper(df, fandom)
            final_sum += init_sum
    else: 
        for fandom in fandom_list: 
            init_sum = fandom_stre_helper(df, fandom, True)
            final_sum += init_sum
            
    return final_sum

def create_fandom_df(data_list):
    '''
    returns a dataframe of each artist who has a fandom name and the sum
    of tweets that contain 
    '''
    indiv_li = []
    fandom_li = []

    for data_dict in data_list:
        artist_names = list(data_dict.keys())

        for indiv in artist_names:
            artist_name = indiv.lower()
            indiv_li.append(artist_name)

            df = data_dict[indiv][0]

            if artist_name == "giselle":
                calc_sum = calc_fandom_strength(df, fandom_names[artist_name], True)
            elif artist_name not in fandom_names.keys():
                calc_sum = 0
            else: 
                calc_sum = calc_fandom_strength(df, fandom_names[artist_name])

            fandom_ratio = calc_sum/len(df)
            fandom_li.append(fandom_ratio)
        
    df = pd.DataFrame({"indiv": indiv_li, "fandom_ratio": fandom_li})
    df = df.sort_values(by="fandom_ratio", ascending=False).reset_index(drop=True)

    return df

def group_artists(tweet_list, data_list):
    all_tweets_df = create_before_cancel_df(tweet_list)
    engage_df = calc_engage_metric(all_tweets_df)

    fandom_df = create_fandom_df(data_list)

    # combine both dataframes into single df
    combined_df = fandom_df.merge(engage_df, on="indiv")

    strong_ps_indivs = list(combined_df[(combined_df["engage_ratio"] >= engagement_threshold) & (
        combined_df["fandom_ratio"] >= fandom_threshold)]["indiv"])
    weak_ps_indivs = list(combined_df[(combined_df["engage_ratio"] < engagement_threshold) | (
        combined_df["fandom_ratio"] < fandom_threshold)]["indiv"])

    return strong_ps_indivs, weak_ps_indivs

def create_parasocial_dfs(out_dir, tweet_list, data_list):
    # initialize variables
    strong_Tox_dfs = []
    weak_Tox_dfs = []

    # group artists into strong vs weak parasocial relationship
    strong_indivs, weak_indivs = group_artists(tweet_list, data_list)

    for data_dict in data_list:
        artist_names = list(data_dict.keys())

        for indiv in artist_names:
            artist_name = indiv.lower()

            toxicity_data = data_dict[indiv][0]

            # preprocess toxic df 
            toxic_df = clean_toxic_df(toxicity_data) # remove invalid values
            toxic_df = convert_dates(toxic_df) # convert to datetime obj
            # group by how many days away from cancel date
            toxic_df = toxic_df.groupby(["created_at"]).mean().reset_index() 
            toxic_df['indiv'] = artist_name

            if artist_name in strong_indivs:
                strong_Tox_dfs.append(toxic_df)
            elif artist_name in weak_indivs:
                weak_Tox_dfs.append(toxic_df)

    final_strong_Tdf = pd.concat(strong_Tox_dfs)
    final_strong_df = final_strong_Tdf.reset_index(drop=True)

    final_weak_Tdf = pd.concat(weak_Tox_dfs)
    final_weak_df = final_weak_Tdf.reset_index(drop=True)

    # create/check folder exists
    out_dir =os.path.join(out_dir,"rq3_ps/")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    final_strong_df.to_csv(out_dir + "strong_ps.csv", index=False)
    final_weak_df.to_csv(out_dir + "weak_ps.csv", index=False)

    

    

            