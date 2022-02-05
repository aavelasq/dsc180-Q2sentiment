import os
from textblob import TextBlob
import pandas as pd

outdir = ".//data/out/"
tempdir = ".//data/temp/"

def textblob_analyzer_polarity(text):
    '''
    calculates polarity sentiment using TextBlob library
    '''
    tweet = TextBlob(text)
    return tweet.sentiment.polarity
    
def calc_textblob_polarity(data, target, cancellation_date):
    '''
    calculates mean polarity before and after controversy date
    outputs line plot and polarity over cancellation period data
    '''
    data = convert_dates(data)
    data["Days Before & After Controversy"] = (data["created_at"] - cancellation_date).dt.days
    data['sentiment polarity'] = data["text"].apply(textblob_analyzer_polarity)
    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['sentiment polarity']


    polarity_output = pol_mean_daily.reset_index()
    csv_file_name = outdir + target + '_meanPolarity.csv'
    polarity_output.to_csv(csv_file_name, index=False)
    
    return pol_mean_daily

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
