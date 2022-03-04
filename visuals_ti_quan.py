import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime 
from eda import convert_dates

cancel_dates = {"lucas": datetime.datetime(2021,8,24), "giselle": datetime.datetime(2021,10,23), 
                "jaemin": datetime.datetime(2021,8,24), "ryujin": datetime.datetime(2021,10,23),
                "dababy": datetime.datetime(2021,7,25), "nicki": datetime.datetime(2021,9,13), 
                "lilbaby": datetime.datetime(2021,7,25), "saweetie": datetime.datetime(2021,9,13),
                "zayn": datetime.datetime(2021,10,28), "doja": datetime.datetime(2020,5,25), 
                "harry": datetime.datetime(2021,10,28), "adele": datetime.datetime(2020,5,25)}

def count_days(row):
    '''
    helper function to count number of days since deplatform date
    '''
    cancel_date = cancel_dates[row["indiv"].lower()]

    return row["created_at"] - cancel_date

def preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, roll_days):

    misinfo_dfs = convert_dates(misinfo_dfs) # convert to datetime obj
    # group by # of days canceled
    misinfo_dfs['days_cancel'] = misinfo_dfs.apply(count_days, axis=1)
    # calculate rolling avg then calculate median
    misinfo_dfs = misinfo_dfs.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    misinfo_dfs["group"] = "misinfo" # label group

    
    discrim_dfs = convert_dates(discrim_dfs) # convert to datetime obj
    # group by # of days canceled
    discrim_dfs['days_cancel'] = discrim_dfs.apply(count_days, axis=1)
    # calculate rolling avg then calculate median
    discrim_dfs = discrim_dfs.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    discrim_dfs["group"] = "discrim" # label group
    
    assualt_dfs = convert_dates(assualt_dfs) # convert to datetime obj
    # group by # of days canceled
    assualt_dfs['days_cancel'] = assualt_dfs.apply(count_days, axis=1)
    # calculate rolling avg then calculate median
    assualt_dfs = assualt_dfs.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    assualt_dfs["group"] = "assualt" # label group
    
    final = pd.concat([misinfo_dfs, discrim_dfs, assualt_dfs])
    return final

def ps_line_plot(out_dir, df, metric):
    '''
    generates line plot based on inputted df
    '''
    plt.figure(figsize = (15,10))
    sns.lineplot(data=df, x="days_cancel", y=metric, hue="group")
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel(str(metric))
    plt.axvline(0, 0.04, 0.99,color="red")

    file_name = str(metric) + "_ti_Line.png"
        
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, bbox_inches='tight')

def create_visuals_quan(arg1, arg2, arg3):
    
    misinfo_dfs = pd.read_csv(arg1)
    discrim_dfs = pd.read_csv(arg2)
    assualt_dfs = pd.read_csv(arg3)


    combined = preprocess_ti_df(misinfo_dfs, discrim_dfs, assualt_dfs, "14d")
    
    # convert timedelta to int 
    combined["days_cancel"] = combined["days_cancel"].dt.days
    
    # makes sure time period is 6 months before and after cancellation date
    combined = combined[(combined["days_cancel"] >= -183) | (combined["days_cancel"] <= 183)]

    combined.to_csv("./data/temp/" + "final_ti.csv", index=False)
    
    plt.clf()
    ps_line_plot("./data/out/", combined, "severe_toxicity")

    plt.clf()
    ps_line_plot("./data/out/", combined, "insult")