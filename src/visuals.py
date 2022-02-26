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

def preprocess_ps_df(strong_df, weak_df, roll_days):
    '''
    combines strong and weak grouped artist dfs into one df
    '''
    strong_df = convert_dates(strong_df) # convert to datetime obj
    # group by # of days canceled
    strong_df['days_cancel'] = strong_df.apply(count_days, axis=1)
    # calculate rolling avg then calculate median
    strong_df = strong_df.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    strong_df["group"] = "strong" # label group

    weak_df = convert_dates(weak_df) # convert to datetime obj
    weak_df['days_cancel'] = weak_df.apply(count_days, axis=1)
    weak_df = weak_df.groupby(by=["days_cancel"]).mean().rolling(roll_days).median().reset_index()
    weak_df["group"] = "weak"

    return pd.concat([strong_df, weak_df]).reset_index(drop=True)

def overall_avgs(toxic_df, vader_df):
    '''
    calculates avg before and after cancellation for input df
    '''
    before_toxic = toxic_df[toxic_df["days_cancel"] < 0].median()
    after_toxic = toxic_df[toxic_df["days_cancel"] > 0].median()
    before_vader = vader_df[vader_df["days_cancel"] < 0].median()
    after_vader = vader_df[vader_df["days_cancel"] > 0].median()

    print(before_toxic)
    print(after_toxic)

def ps_line_plot(out_dir, df, metric):
    '''
    generates line plot based on inputted df
    '''
    plt.figure(figsize = (15,10))
    sns.lineplot(data=df, x="days_cancel", y=metric, hue="group")
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel(str(metric))
    plt.axvline(0, 0.04, 0.99,color="red")

    file_name = str(metric) + "_psLine.png"
    out_path = os.path.join(out_dir, file_name)
    plt.savefig(out_path, bbox_inches='tight')

def create_visuals(arg1, arg2):
    strong_ps_df = pd.read_csv(arg1)
    weak_ps_df = pd.read_csv(arg2)

    # preprocess data
    toxic_ps_df = preprocess_ps_df(strong_ps_df, weak_ps_df, "14d")[[
        "days_cancel", "severe_toxicity", "insult", "group"]]
    vader_ps_df = preprocess_ps_df(strong_ps_df, weak_ps_df, "28d")[[
        "days_cancel", "Compound", "Negative", "group"]]
    # convert timedelta to int 
    toxic_ps_df["days_cancel"] = toxic_ps_df["days_cancel"].dt.days
    vader_ps_df["days_cancel"] = vader_ps_df["days_cancel"].dt.days
    # makes sure time period is 6 months before and after cancellation date
    toxic_ps_df = toxic_ps_df[(toxic_ps_df["days_cancel"] >= -183) | (toxic_ps_df["days_cancel"] <= 183)]
    vader_ps_df = vader_ps_df[(vader_ps_df["days_cancel"] >= -183) | (vader_ps_df["days_cancel"] <= 183)]
    toxic_ps_df.to_csv("./data/temp/toxic_ps.csv")
    vader_ps_df.to_csv("./data/temp/vader_ps.csv")
    overall_avgs(toxic_ps_df, vader_ps_df)

    plt.clf()
    ps_line_plot("./data/out/", toxic_ps_df, "severe_toxicity")
    plt.clf()
    ps_line_plot("./data/out/", toxic_ps_df, "insult")
    plt.clf()
    ps_line_plot("./data/out/", vader_ps_df, "Compound")
    plt.clf()
    ps_line_plot("./data/out/", vader_ps_df, "Negative")

