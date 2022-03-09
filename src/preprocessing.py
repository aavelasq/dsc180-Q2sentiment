import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
import os

from eda import convert_dates

def create_toxicLinePlot(out_dir, df, attribute_type, indiv):
    '''
    creates line graphs from data generated from toxicity script
    '''
    if attribute_type == 'severe_toxicity': 
        severe_toxicityLevels = df['severe_toxicity'] # mean severe toxicty per time window
        severe_toxicity_df = severe_toxicityLevels.reset_index().rename(
            columns={"created_at": "Date", "severe_toxicity": "Mean Severe Toxicity"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=severe_toxicity_df, x="Date", y="Mean Severe Toxicity")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Severe Toxicity Levels")

        file_name = indiv + "_severeToxicityPlot.png"
        out_path = os.path.join(out_dir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'insult': 
        insultLevels = df['insult'] # mean insult per time window
        insult_df = insultLevels.reset_index().rename(
            columns={"created_at": "Date", "insult": "Mean Insult Levels"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=insult_df, x="Date", y="Mean Insult Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Insult Levels")

        file_name = indiv + "_insultPlot.png"
        out_path = os.path.join(out_dir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

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

def compute_rolling_avg(df):
    if 'toxicity' in df.columns: 
        # clean df first
        cleaned_df = convert_dates(clean_toxic_df(df))
    else:
        cleaned_df = df

    # rolling average (mean) interval set to 7 days / a week
    rolling_avg_df = cleaned_df.groupby("created_at").mean().rolling("7d").mean()

    return rolling_avg_df

def calculate_avgs(data_dict, out_dir, temp_dir):
    artist_names = list(data_dict.keys())

    for indiv in artist_names:
        toxicity_data = data_dict[indiv][0]
        # vader_data = data_dict[indiv][1]
        # cancel_date = data_dict[indiv][2]

        toxicity_df = convert_dates(toxicity_data)
        # vader_df = convert_dates(vader_data)

        # computes rolling average on toxicity df
        toxic_roll_df = compute_rolling_avg(toxicity_df)

        # creates line graphs from toxciity rolling avg data 
        # create_toxicLinePlot(out_dir, roll_df, "severe_toxicity", indiv)
        # create_toxicLinePlot(out_dir, roll_df, "insult", indiv)

        # saves to temp data folder 
        temp_path = temp_dir + indiv + "_toxicRollAvg.csv"
        toxic_roll_df.reset_index().to_csv(temp_path)

        # computes rolling average on vader df
        # vader_roll_df = compute_rolling_avg(vader_df)

        # saves to temp data folder 
        temp_path = temp_dir + indiv + "_vaderRollAvg.csv"
        # vader_roll_df.reset_index().to_csv(temp_path)