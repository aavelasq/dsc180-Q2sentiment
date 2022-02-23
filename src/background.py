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

def create_medianLinePlot(out_dir, can_df, con_df, category, metric):
    '''
    generate and save median line plots for specified metric and
    category for cancelled and control groups
    '''
    if category == "kpop":
        c_name = "K-Pop"
    elif category == "hiphop":
        c_name = "Hip Hop"
    elif category == "pop" or category == "female" or category == "male":
        c_name = str.upper(category[0]) + category[1:]

    plt.figure(figsize = (10,5))
    sns.lineplot(data=can_df, x="Days Before & After Controversy", y=metric)
    sns.lineplot(data=con_df, x="Days Before & After Controversy", y=metric)
    plt.xlabel('# Days Before and After Cancellation')
    plt.title(c_name + " Cancelled vs Control Group Median " + metric + " Levels")
    plt.legend(["Cancelled", "Control"])
    if metric == "severe_toxicity":
        plt.ylabel("Median Severe Toxicity Levels")
    elif metric == "insult":
        plt.ylabel("Median Insult Levels")
    elif metric == "Compound":
        plt.ylabel("Median Compound Polarity Levels")
    elif metric == "Negative":
        plt.ylabel("Median Negative Polarity Levels")
    file_name = category + "_median_" + metric + "Plot.png"
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, bbox_inches='tight')


def transform_data(data_list, metric):
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
        
        roll_df["Days Before & After Controversy"] = (roll_df["created_at"] - cancel_date).dt.days
        artist_dict[indiv] = roll_df[["Days Before & After Controversy", metric]]
    
    return artist_dict


def combine_data(artist_dict, female_list=None, male_list=None, gender=None):
    '''
    concatenate data according to what group is provided
    '''
    if gender == "female":
        cat_control = pd.concat([artist_dict[female_kpop_list[1]], artist_dict[female_hiphop_list[1]], artist_dict[female_pop_list[1]]])
        cat_cancelled = pd.concat([artist_dict[female_kpop_list[0]], artist_dict[female_hiphop_list[0]], artist_dict[female_pop_list[0]]])
        
    elif gender == "male":
        cat_control =  pd.concat([artist_dict[male_kpop_list[1]], artist_dict[male_hiphop_list[1]], artist_dict[male_pop_list[1]]])
        cat_cancelled = pd.concat([artist_dict[male_kpop_list[0]], artist_dict[male_hiphop_list[0]], artist_dict[male_pop_list[0]]])
    
    else:
        cat_cancelled = pd.concat([artist_dict[female_list[0]], artist_dict[male_list[0]]])
        cat_control = pd.concat([artist_dict[female_list[1]], artist_dict[male_list[1]]])
        cat_cancelled_median = cat_cancelled.groupby("Days Before & After Controversy").median()
        cat_control_median = cat_control.groupby("Days Before & After Controversy").median()
        
    cat_cancelled_median = cat_cancelled.groupby("Days Before & After Controversy").median()
    cat_control_median = cat_control.groupby("Days Before & After Controversy").median()
    return [cat_cancelled_median, cat_control_median]

def days_after(df, metric):
    '''
    helper function to get the number of days where the median metric returns to 
    pre-controversy levels
    '''
    df = df.reset_index()
    contoversy_med = df[df["Days Before & After Controversy"] == 0][metric].item()
    k_stats_aft_con = df[df["Days Before & After Controversy"] > 0]
    try:
        first_occurence = k_stats_aft_con[k_stats_aft_con[metric] <= contoversy_med].iloc[0]
    except:
        d = {"Days Before & After Controversy": "Hasn't been reached", metric: None}
        first_occurence = pd.Series(data=d)
    return first_occurence

def calculate_median(data_list, out_dir, temp_dir, metric):

    artist_dict = transform_data(data_list,metric)
    all_artist = {"kpop":[female_kpop_list, male_kpop_list], "hiphop":[female_hiphop_list, male_hiphop_list], "pop":[female_pop_list, male_pop_list],
                    "female":None, "male":None}

    # iterate through all artists
    for k,v in all_artist.items():
        # combine data by gender or industry
        if k == "female" or k == "male":
            cat_meds = combine_data(artist_dict, gender=k)
        else:
            cat_meds = combine_data(artist_dict, v[0], v[1])  

        # combined data for cancelled groups
        cat_cancelled_median = cat_meds[0]
        # combined data for control groups
        cat_control_median = cat_meds[1]

        if k == "female" or k == "male" or k == "hiphop" :
            cat_cancelled_median = cat_meds[0].rolling(5).median()
            cat_control_median = cat_meds[1].rolling(5).median()

        # generate line plot of median metric level for specific group   
        create_medianLinePlot(out_dir, cat_cancelled_median, cat_control_median, k , metric)

        # save df that creates the line plot
        cat_cancelled_median.reset_index().to_csv(temp_dir +  k + "_CancelledMedian.csv")
        cat_control_median.reset_index().to_csv(temp_dir +  k +"_ControlMedian.csv")
        
        # calculate the number of days until median metric drops below controversy date levels
        return_to_med_can = days_after(cat_cancelled_median, metric)
        return_to_med_con = days_after(cat_control_median, metric)
        
        # combine control and cancelled
        final_days_after = pd.concat([return_to_med_can.rename("cancelled"),return_to_med_con.rename("control")], axis=1)

        # save the df above
        final_days_after.reset_index().to_csv(temp_dir  + k  + "_" + metric + "_" + "daysReturnMed.csv")




    

    

    
    

    

