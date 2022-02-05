import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from polarity_script import convert_dates

tempdir = ".//data/temp/"
outdir = ".//data/out/"

def polarityFunc(data, target, cancellation_date):

    data = convert_dates(data)
    data["Days Before & After Controversy"] = (data["created_at"] - cancellation_date).dt.days

    main_df = data
    analyser = SentimentIntensityAnalyzer()
    scores = []

    for tweet in data['text']: 
        polarity_val = analyser.polarity_scores(tweet)
        scores.append(polarity_val)
    
    print("Data Collected: ", len(scores))
    temp_df = pd.DataFrame(scores)

    data['Compound'] = temp_df['compound']
    data['Negative'] = temp_df['neg']
    data['Neutral'] = temp_df['neu']
    data['Positive'] = temp_df['pos']

    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['Compound']
    
    file_name = outdir + target + '_vaderPolarity.csv'
    vader_output = pol_mean_daily.reset_index()
    vader_output.to_csv(file_name, index=False)
    main_df.to_csv(file_name, index=False)

    return pol_mean_daily

