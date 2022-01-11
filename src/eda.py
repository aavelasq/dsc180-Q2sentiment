import pandas as pd 
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import os

cancellation_date = datetime.datetime(2021, 8, 24)
outdir = ".//data/out"
tempdir = ".//data/temp"

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

def count_days(date, cancel_date):
    '''
    helper function to count number of days since deplatform date
    '''
    return date - cancel_date

def user_activity_levels(data, cancel_date):
    '''
    measures posting activity levels by counting the number of tweets
    that occur per each time window (1 day)
    '''
    groupedUsers = data[['created_at', 'text']].groupby(by='created_at')

    num_tweets = groupedUsers.count()['text'] # number of tweets per time window

    df = num_tweets.reset_index().rename(
        columns={"created_at": "Date", "text": "# Tweets"})

    df['Date'] = df['Date'].apply(
        lambda x: count_days(x, cancel_date)).dt.days

    # convert df to csv
    out_path = os.path.join(tempdir, "userActivityLevels.csv")
    df.to_csv(out_path)

    return df

def create_userActivity_graph(df):
    '''
    creates graph for user activity
    '''
    sns.lineplot(data=df, x="Date", y="# Tweets")
    plt.xlabel('# Days Before and After Cancellation')
    plt.title("Volume of Tweets")

    out_path = os.path.join(outdir, "userActivityPlot.png")
    plt.savefig(out_path, bbox_inches='tight')

def numOfTweets(df, cancel_date):
    '''
    calculates number of tweets before and after date
    '''
    if cancel_date == 0:
        before_df = df[df['Date'] < cancel_date]
        on_date_df = df[df['Date'] == cancel_date]
        after_df = df[df['Date'] > cancel_date]
    else: 
        before_df = df[df['created_at'] < cancel_date]
        on_date_df = df[df['created_at'] == cancel_date]
        after_df = df[df['created_at'] > cancel_date]

    num_df = pd.DataFrame(data={"Before": [len(before_df)], "On Date": [len(on_date_df)],"After": [len(after_df)]})

    return num_df

def calculate_stats(data, test=False):
    df = convert_dates(data)

    if test == False:
        # create csvs out of data
        userActivity_df = user_activity_levels(df, cancellation_date)
        # counts number of tweets before and after deplatforming 
        totalTweets = numOfTweets(df, cancellation_date)
    else:
        # userActivity_df = user_activity_levels(df, test_date)
        # totalTweets = numOfTweets(df, test_date)
        print("test")

    out_path = os.path.join(outdir, "numOfTweetsBefAft.csv")
    totalTweets.to_csv(out_path)
    # aggregate_twitter_vals()

    # create graphs + save as pngs
    create_userActivity_graph(userActivity_df)