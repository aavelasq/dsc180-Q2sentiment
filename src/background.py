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

def create_medianLinePlot(out_dir, df, category, metric, group):
    '''
    generate and save median line plots for specified metric and
    category for cancelled and control groups
    '''
    plt.figure(figsize = (10,5))
    sns.lineplot(data=df, x="Days Before & After Controversy", y=metric)
    plt.xlabel('# Days Before and After Cancellation')
    plt.title(group + " Median " + metric + " Levels")

    file_name = category + "_" + group + "_median_" + metric + "Plot.png"
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
    
    print(artist_names)
    artist_dict = {}

    for indiv in artist_names:
        print(indiv)
        print(metric)

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
        # female_comb = pd.concat([artist_dict[female_list[0]], artist_dict[female_list[1]]])
        # male_comb = pd.concat([artist_dict[male_list[0]], artist_dict[male_list[1]]])
        # cat_comb = pd.concat([female_comb, male_comb])
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
    first_occurence = k_stats_aft_con[k_stats_aft_con[metric] <= contoversy_med].iloc[0]
    
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

        # generate line plot of median metric level for specific group   
        create_medianLinePlot(out_dir, cat_cancelled_median, k, metric, "Cancelled")
        create_medianLinePlot(out_dir, cat_control_median, k, metric, "Control")
        
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
        # return_to_med_can.reset_index().to_csv(temp_dir  + k + "_Cancelled" + "_" + metric + "_" + "daysReturnMed.csv")
        # return_to_med_con.reset_index().to_csv(temp_dir  + k + "_Control" + "_" + metric + "_" + "daysReturnMed.csv")





    

    

    
    

    

