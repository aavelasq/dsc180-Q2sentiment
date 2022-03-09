import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os
import datetime
from polarity_script import convert_dates
from preprocessing import compute_rolling_avg


# CHANGE DATE DEPENDING ON INDIVIDUAL 
maleKpop_cancel_date = datetime.datetime(2021, 8, 24) # LUCAS
femaleKpop_cancel_date = datetime.datetime(2021, 10, 23) # GISELLE

maleHH_cancel_date = datetime.datetime(2021, 7, 25) # DABABY
femaleHH_cancel_date = datetime.datetime(2021, 9, 13) # NICKI

malePop_cancel_date = datetime.datetime(2021, 8, 28) # ZAYN
femalePop_cancel_date = datetime.datetime(2020, 5, 25) # DOJA CAT

# list of cancelled individuals 
male_kpop_list = ['JAEMIN', 'LUCAS']
female_kpop_list = ['GISELLE', 'RYUJIN']

male_hiphop_list = ['DABABY', 'LILBABY']
female_hiphop_list = ['NICKI', 'SAWEETIE']

male_pop_list = ['ZAYN', 'HARRY']
female_pop_list = ['DOJA', 'ADELE']

def create_medianLinePlot(out_dir, df, category, metric, hue):
    '''
    generate and save median line plots for specified metric and
    category for cancelled and control groups
    '''
    if category == "genre":
        c_name = "Genre"
        med = "Median "
    elif category == "sex":
        c_name = "Sex"
        med = "Median " 
    elif category == "all":
        c_name = "All Canceled Artists "
        med = ""
    
    if metric == "severe_toxicity":
        y_label = "Severe Toxicity"
    elif metric == "insult":
        y_label = "Insult"

    plt.figure(figsize = (10,5))
    sns.lineplot(data=df, x="Days Before & After Controversy", y=metric, hue=hue)
    plt.axvline(0, 0.01, 0.99,color="red")
    plt.xlabel('Days Since Cancellation')
    plt.ylabel(med + y_label + " Levels")
    plt.title(med + y_label + " Levels By " + c_name)
    file_name = category + "_median_" + metric + "Plot.png"
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, bbox_inches='tight')


def transform_data(data_list, metric, test):
    '''
    transform data to get rolling average
    '''
    artist_names = list()
    data_dict = {}
    for d in data_list:
        artist_names += d.keys()
        data_dict.update(d)
    
    artist_dict = {}

    for indiv in artist_names:
        if metric == "insult" or metric == "severe_toxicity":
            data = data_dict[indiv][0]
        elif metric == "Compound" or metric == "Negative":
            data = data_dict[indiv][1]
        df = convert_dates(data)

        # computes rolling average
        roll_df = compute_rolling_avg(df).reset_index()

        if indiv in male_kpop_list:
            cancel_date = maleKpop_cancel_date
        elif indiv in female_kpop_list:
            cancel_date = femaleKpop_cancel_date
        elif indiv in male_hiphop_list:
            cancel_date = maleHH_cancel_date
        elif indiv in female_hiphop_list:
            cancel_date = femaleHH_cancel_date
        elif indiv in male_pop_list:
            cancel_date = malePop_cancel_date
        elif indiv in female_pop_list:
            cancel_date = femalePop_cancel_date

        if test:
            cancel_date = datetime.datetime(2022, 2, 6)
        
        roll_df["Days Before & After Controversy"] = (roll_df["created_at"] - cancel_date).dt.days
        artist_dict[indiv] = roll_df[["Days Before & After Controversy", metric]]
    
    return artist_dict


def combine_data(artist_dict, female_list=None, male_list=None, gender=None):
    '''
    concatenate data according to what group is provided
    '''
    if gender == "female":
        cat_cancelled = pd.concat([artist_dict[female_kpop_list[0]], artist_dict[female_hiphop_list[0]], artist_dict[female_pop_list[0]]])
        
    elif gender == "male":
        cat_cancelled = pd.concat([artist_dict[male_kpop_list[0]], artist_dict[male_hiphop_list[0]], artist_dict[male_pop_list[0]]])
    
    else:
        cat_cancelled = pd.concat([artist_dict[female_list[0]], artist_dict[male_list[0]]])
        
    cat_cancelled_median = cat_cancelled.groupby("Days Before & After Controversy").median()

    return cat_cancelled_median.reset_index()

def days_after(df, metric):
    '''
    helper function to get the number of days where the median metric returns to 
    pre-controversy levels
    '''
    df = df.reset_index()
    day_of_con = 0
    while day_of_con not in df["Days Before & After Controversy"].values:
        day_of_con -= 1

    # calculate days after for grouped category df
    if "group" in df:
        if "male" in df["group"].values:
            m_df = df[df["group"] == "male"]
            f_df = df[df["group"] == "female"]
            g_list = [m_df, f_df]

        elif "pop" in df["group"].values:
            k_df = df[df["group"] == "kpop"]
            h_df = df[df["group"] == "hiphop"]
            p_df = df[df["group"] == "pop"]
            g_list = [k_df, h_df, p_df]
        g_df = pd.DataFrame()

        for df in g_list:
                contoversy_med = df[df["Days Before & After Controversy"] == day_of_con][metric].item()
                k_stats_aft_con = df[df["Days Before & After Controversy"] > 0]
                try:
                    first_occurence = k_stats_aft_con[k_stats_aft_con[metric] < contoversy_med].iloc[0]
                except:
                    d = {"Days Before & After Controversy": "Hasn't been reached", metric: None}
                    first_occurence = pd.Series(data=d)
                
                if len(g_df) == 0:
                    g_df = first_occurence.rename(df["group"].iloc[0]).drop(labels=["group", "index"])
                else:
                    g_df = pd.concat([g_df, first_occurence.rename(df["group"].iloc[0]).drop(labels=["group", "index"])], axis=1) 
        return g_df  

    # calculate days after return to median for other dfs
    contoversy_med = df[df["Days Before & After Controversy"] == day_of_con][metric].item()

    k_stats_aft_con = df[df["Days Before & After Controversy"] > 0]
    try:
        first_occurence = k_stats_aft_con[k_stats_aft_con[metric] < contoversy_med].iloc[0]
    except:
        d = {"Days Before & After Controversy": "Hasn't been reached", metric: None}
        first_occurence = pd.Series(data=d)
    return first_occurence
    

def calculate_median(data_list, out_dir, temp_dir, metric, test=False):
    #clean/transform all artist data & add to dict
    artist_dict = transform_data(data_list,metric,test)
    all_artist = {"kpop":[female_kpop_list, male_kpop_list], "hiphop":[female_hiphop_list, male_hiphop_list], "pop":[female_pop_list, male_pop_list],
                    "female":None, "male":None}
    # make empty dfs
    all_can_df = pd.DataFrame()
    can_all_art_ret = pd.DataFrame()
    fm_df = pd.DataFrame()
    khp_df = pd.DataFrame()

    # iterate through all artists
    for k,v in all_artist.items():
        
        # combine data by gender or industry
        if k == "female" or k == "male":
            cat_cancelled_median = combine_data(artist_dict, gender=k)
        else:
            # retrieve male and female canceled artists
            f_name = v[0][0]
            m_name = v[1][0]
            can_female_df =  artist_dict[f_name]
            can_male_df = artist_dict[m_name]
            # add identifier column
            can_female_df["artist"] = f_name
            can_male_df["artist"] = m_name

            # append artist df to main df
            if len(all_can_df) == 0:
                all_can_df = can_female_df
                all_can_df = pd.concat([all_can_df, can_male_df], ignore_index=True) 
            else:
                all_can_df = pd.concat([all_can_df, can_female_df, can_male_df], ignore_index=True)  

            # calculate days returning to median for artists
            can_female_return = days_after(can_female_df.drop(columns=["artist"]), metric)
            can_male_return = days_after(can_male_df.drop(columns=["artist"]), metric)
            
            comb_can_ret = pd.concat([can_female_return.rename(f_name),can_male_return.rename(m_name)], axis=1)

            # append artist return to median df to main df
            if len(can_all_art_ret) == 0:
                can_all_art_ret = comb_can_ret
            else:
                can_all_art_ret = pd.concat([can_all_art_ret, comb_can_ret], axis=1)

            cat_cancelled_median = combine_data(artist_dict, v[0], v[1])  
        if test == False:
            if k == "hiphop" or k == "female":
                cat_cancelled_median = cat_cancelled_median.rolling(5).median()

        # add indicator column
        cat_cancelled_median["group"] = k

        # append group df to main df
        if k == "female" or k == "male":
            if len(fm_df) == 0:
                fm_df = cat_cancelled_median
            else:
                fm_df = pd.concat([fm_df, cat_cancelled_median], ignore_index=True)
        else:
            if len(khp_df) == 0:
                khp_df = cat_cancelled_median
            else:
                khp_df = pd.concat([khp_df, cat_cancelled_median], ignore_index=True)

    # create/check folders exist
    out_dir = os.path.join(out_dir,"rq2_bg/")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    temp_dir = os.path.join(temp_dir,"rq2_bg/")
    if not os.path.isdir(temp_dir):
        os.mkdir(temp_dir)

    # plotting line plots for groups and artists
    create_medianLinePlot(out_dir, all_can_df, "all" , metric, "artist")
    create_medianLinePlot(out_dir, fm_df, "sex" , metric, "group")
    create_medianLinePlot(out_dir, khp_df, "genre" , metric, "group")

    # saving plot data to csv
    all_can_df.reset_index().to_csv(temp_dir +   "all_" + metric + "_Cancelled.csv")
    fm_df.reset_index().to_csv(temp_dir +   "sex_" + metric + "_CancelledMedian.csv")
    khp_df.reset_index().to_csv(temp_dir + "genre_" + metric + "_CancelledMedian.csv")

    # calculating number of days return to median to groups
    return_to_med_fm = days_after(fm_df, metric)
    return_to_med_khp = days_after(khp_df, metric)

    # saving data to csv
    return_to_med_fm.reset_index().to_csv(temp_dir  + "sex_" + metric + "_" + "daysReturnMed.csv")
    return_to_med_khp.reset_index().to_csv(temp_dir  + "genre_" + metric + "_" + "daysReturnMed.csv")
    can_all_art_ret.drop("index").reset_index().to_csv(temp_dir + "all_canceled_artists_" + metric+ "Return.csv")


    


    

    

    
    

    

