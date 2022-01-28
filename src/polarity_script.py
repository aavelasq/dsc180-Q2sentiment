import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os
from textblob import TextBlob
from eda import convert_dates

# CHANGE DATE DEPENDING ON INDIVIDUAL
cancellation_date = datetime.datetime(2021, 7, 25)
outdir = ".//data/out/"
tempdir = ".//data/temp/"

def textblob_analyzer_polarity(text):
    '''
    calculates polarity sentiment using TextBlob library
    '''
    tweet = TextBlob(text)
    return tweet.sentiment.polarity
    
def textblob_sentiment(data, target):
    '''
    calculates mean polarity before and after controversy date
    outputs line plot and polarity over cancellation period data
    '''
    data = convert_dates(data)
    data["Days Before & After Controversy"] = (data["created_at"] - cancellation_date).dt.days
    data['sentiment polarity'] = data["text"].apply(textblob_analyzer_polarity)
    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['sentiment polarity']

    sns.lineplot(data=pol_mean_daily)
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel("Polarity")
    plt.title("Mean Twitter Polarity of " + target + " Before and After Controversy")
    plt.axvline(0, 0.04, 0.99,color="red")
    png_file_name = target + "_textblob_polarity1.png"
    out_path_png = os.path.join(outdir, png_file_name)
    plt.savefig(out_path_png,dpi=300, bbox_inches = "tight")
    plt.close()

    pol_mean_daily = pol_mean_daily.reset_index()
    csv_file_name = tempdir + target + '_meanPolarity.csv'
    pol_mean_daily.to_csv(csv_file_name, index=False)
