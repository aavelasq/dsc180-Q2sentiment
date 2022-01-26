import pandas as pd
import pandas.util.testing as tm
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import matplotlib.dates as mdates
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tempdir = "/Users/nikithagopal/Documents/dsc30-pa1/dsc180-Q2sentiment/data/temp/"

def polarityFunc(data, target):

    main_df = data
    tweet_dict = {}
    analyser = SentimentIntensityAnalyzer()
    scores = []
    counter = 0
    for tweet in data['text']: 
        polarity_val = analyser.polarity_scores(tweet)
        scores.append(polarity_val)

        if counter/1000 == 0:
            print('completed:', str(counter))
        counter += 1
    
    file_name = tempdir + target + '_vaderPolarity.csv'
    
    print(len(scores))
    temp_df = pd.DataFrame(scores)

    data['Compound'] = temp_df['compound']
    data['Negative'] = temp_df['neg']
    data['Neutral'] = temp_df['neu']
    data['Positive'] = temp_df['pos']
    
    main_df.to_csv(file_name, index=False)

