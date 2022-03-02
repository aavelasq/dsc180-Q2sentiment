import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
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
    cancel_date = cancel_dates[row["indiv"]]

    return row["created_at"] - cancel_date

def preprocess_ps_df(strong_df, weak_df, roll_days, canceled=False):
    '''
    combines strong and weak grouped artist dfs into one df
    '''
    strong_df = convert_dates(strong_df) # convert to datetime obj
    # group by # of days canceled
    strong_df['days_cancel'] = strong_df.apply(count_days, axis=1)
    # subsets df based on canceled or control group 
    if canceled == True:
        strong_df = strong_df[(strong_df['indiv'] == "lucas") | (strong_df['indiv'] == "giselle") | (strong_df['indiv'] == "nicki")]
    elif canceled == False:
        strong_df = strong_df[(strong_df['indiv'] == "jaemin") | (strong_df['indiv'] == "ryujin")]
    # calculate rolling avg then calculate median
    strong_df = strong_df.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    strong_df["group"] = "strong" # label group

    weak_df = convert_dates(weak_df) # convert to datetime obj
    weak_df['days_cancel'] = weak_df.apply(count_days, axis=1)
    if canceled == True:
        weak_df = weak_df[(weak_df['indiv'] == "zayn") | (weak_df['indiv'] == "doja") | (weak_df['indiv'] == "dababy")]
    elif canceled == False:
        weak_df = weak_df[(weak_df['indiv'] == "harry") | (weak_df['indiv'] == "adele") | (weak_df['indiv'] == "lil baby") | (weak_df['indiv'] == "saweetie")]
    weak_df = weak_df.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    weak_df["group"] = "weak"

    return pd.concat([strong_df, weak_df]).reset_index(drop=True)

def overall_avgs(toxic_df):
    '''
    calculates avg before and after cancellation for input df
    '''
    before_toxic = toxic_df[toxic_df["days_cancel"] < 0].groupby(by="group").median()
    after_toxic = toxic_df[toxic_df["days_cancel"] > 0].groupby(by="group").median()

    print("BEFORE CANCELLATION")
    print(before_toxic)
    print()
    print("AFTER CANCELLATION")
    print(after_toxic)

def ps_line_plot(out_dir, df, metric, canceled=False):
    '''
    generates line plot based on inputted df
    '''
    plt.figure(figsize = (15,10))
    sns.lineplot(data=df, x="days_cancel", y=metric, hue="group")
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel(str(metric))
    plt.axvline(0, 0.04, 0.99,color="red")

    if canceled == True:
        file_name = str(metric) + "_cancel_psLine.png"
    else: 
        file_name = str(metric) + "_control_psLine.png"
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, bbox_inches='tight')

def combine_dfs(strong_df, weak_df, canceled=False):
    # preprocess data
    toxic_ps_df = preprocess_ps_df(strong_df, weak_df, "14d", canceled)[[
        "days_cancel", "severe_toxicity", "insult", "group"]]
    # convert timedelta to int 
    toxic_ps_df["days_cancel"] = toxic_ps_df["days_cancel"].dt.days
    # makes sure time period is 6 months before and after cancellation date
    toxic_ps_df = toxic_ps_df[(toxic_ps_df["days_cancel"] >= -183) | (toxic_ps_df["days_cancel"] <= 183)]

    return toxic_ps_df

def create_visuals(arg1, arg2):
    '''
    creates line plots and dfs based on strong and weak parasocial relationship
    groupings
    '''
    strong_ps_df = pd.read_csv(arg1)
    weak_ps_df = pd.read_csv(arg2)

    # for canceled indivs
    canceled_ps_df = combine_dfs(strong_ps_df, weak_ps_df, True)
    canceled_ps_df.to_csv("./data/temp/cancel_toxic_ps.csv")
    overall_avgs(canceled_ps_df)

    plt.clf()
    ps_line_plot("./data/out/", canceled_ps_df, "severe_toxicity", True)
    plt.clf()
    ps_line_plot("./data/out/", canceled_ps_df, "insult", True)

    # # for control indivs
    # control_ps_df = combine_dfs(strong_ps_df, weak_ps_df, False)
    # control_ps_df.to_csv("./data/temp/control_toxic_ps.csv")
    # overall_avgs(control_ps_df)

    # plt.clf()
    # ps_line_plot("./data/out/", control_ps_df, "severe_toxicity", False)
    # plt.clf()
    # ps_line_plot("./data/out/", control_ps_df, "insult", False)
