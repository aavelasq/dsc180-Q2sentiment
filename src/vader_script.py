<<<<<<< HEAD
import os
import pandas as pd
import pandas.util.testing as tm
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import datetime
import matplotlib.dates as mdates
from eda import convert_dates
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tempdir = ".//data/temp/"
outdir = ".//data/out/"
# CHANGE DATE DEPENDING ON INDIVIDUAL
cancellation_date = datetime.datetime(2021, 10, 28)

def plotPolarity(meanPolar, target):
    '''
    produces line plot tracking polarity of tweets relating to
    an individual before and after a controvery date
    '''

    sns.lineplot(data=meanPolar)
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel("Polarity")
    plt.title("Mean Twitter Polarity of " + target + " Before and After Controversy")
    plt.axvline(0, 0.04, 0.99,color="red")
    png_file_name = target + "_vader_polarity1.png"
    out_path_png = os.path.join(outdir, png_file_name)
    plt.savefig(out_path_png,dpi=300, bbox_inches = "tight")
    plt.close()


def polarityFunc(data, target):
    '''
    calculates mean polarity before and after controversy date
    outputs line plot and polarity over cancellation period data 
    using Vader Sentiment library
    '''

    data = convert_dates(data)
    data["Days Before & After Controversy"] = (data["created_at"] - cancellation_date).dt.days

    analyser = SentimentIntensityAnalyzer()
    scores = []

    for tweet in data['text']: 
        polarity_val = analyser.polarity_scores(tweet)
        scores.append(polarity_val)
    print(len(scores))

=======
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tempdir = ".//data/temp/"

def polarityFunc(data, target):

    main_df = data
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
>>>>>>> 47f12acb9f336f8398c9e00b439721a410314d9f
    temp_df = pd.DataFrame(scores)

    data['Compound'] = temp_df['compound']
    data['Negative'] = temp_df['neg']
    data['Neutral'] = temp_df['neu']
    data['Positive'] = temp_df['pos']
<<<<<<< HEAD

    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['Compound']
    
    plotPolarity(pol_mean_daily, target)

    file_name = tempdir + target + '_vaderPolarity.csv'
    pol_mean_daily = pol_mean_daily.reset_index()
    pol_mean_daily.to_csv(file_name, index=False)
=======
    
    main_df.to_csv(file_name, index=False)

>>>>>>> 47f12acb9f336f8398c9e00b439721a410314d9f
