import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import os

base_outdir = ".//data/out/"

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

def user_activity_levels(data, target, cancel_date, tempdir):
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
    file_path = target + "_userActivityLevels.csv"
    out_path = os.path.join(tempdir, file_path)
    df.to_csv(out_path)

    return df

def create_userActivity_graph(df, target, base_outdir):
    '''
    creates graph for user activity
    '''
    sns.lineplot(data=df, x="Date", y="# Tweets")
    plt.xlabel('# Days Before and After Cancellation')
    plt.title("Volume of Tweets")

    file_path = target + "_userActivityPlot.png"

    out_path = os.path.join(base_outdir, file_path)
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

def createToxicityLines(df, attribute_type, indiv, base_outdir):
    '''
    creates line graphs from data generated from toxicity script
    '''
    if attribute_type == 'toxicity': 
        toxicityLevels = df.mean()['toxicity'] # mean toxicity per time window
        toxicity_df = toxicityLevels.reset_index().rename(
            columns={"created_at": "Date", "toxicity": "Mean Toxicity"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=toxicity_df, x="Date", y="Mean Toxicity")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Toxicity Levels")

        file_name = indiv + "_toxicityPlot.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'severe_toxicity': 
        severe_toxicityLevels = df.mean()['severe_toxicity'] # mean severe toxicty per time window
        severe_toxicity_df = severe_toxicityLevels.reset_index().rename(
            columns={"created_at": "Date", "severe_toxicity": "Mean Severe Toxicity"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=severe_toxicity_df, x="Date", y="Mean Severe Toxicity")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Severe Toxicity Levels")

        file_name = indiv + "_severeToxicityPlot.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'insult': 
        insultLevels = df.mean()['insult'] # mean insult per time window
        insult_df = insultLevels.reset_index().rename(
            columns={"created_at": "Date", "insult": "Mean Insult Levels"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=insult_df, x="Date", y="Mean Insult Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Insult Levels")

        file_name = indiv + "_insultPlot.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'profanity': 
        profanityLevels = df.mean()['profanity'] # mean profanity per time window
        profanity_df = profanityLevels.reset_index().rename(
            columns={"created_at": "Date", "profanity": "Mean Profanity Levels"})

        plt.figure(figsize = (10,5))
        sns.lineplot(data=profanity_df, x="Date", y="Mean Profanity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Mean Profanity Levels")

        file_name = indiv + "_profanityPlot.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

def month_func(month_num):
    '''
    helper function to convert month numbers to actual names
    '''
    month_li = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    return month_li[month_num - 1]

def createToxicityBoxPlots(df, attribute_type, indiv):
    '''
    creates box plot graphs based on toxicity values 
    '''
    copy_df = df.copy()
    copy_df['Month'] = copy_df['created_at'].dt.month
    copy_df['Month'] = copy_df['Month'].apply(month_func)

    if attribute_type == 'toxicity': 
        copy_df = copy_df.rename(columns={"toxicity": "Toxicity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Toxicity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Toxicity Levels")

        file_name = indiv + "_BoxToxicity.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'severe_toxicity': 
        copy_df = copy_df.rename(columns={"severe_toxicity": "Severe Toxicity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Severe Toxicity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Severe Toxicity Levels")

        file_name = indiv + "_BoxSevToxic.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'insult': 
        copy_df = copy_df.rename(columns={"insult": "Insult Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Insult Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Insult Levels")

        file_name = indiv + "_BoxInsult.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

    if attribute_type == 'profanity': 
        copy_df = copy_df.rename(columns={"profanity": "Profanity Levels"})
        sns.boxplot(data=copy_df, x="Month", y="Profanity Levels")
        plt.xlabel('# Days Before and After Cancellation')
        plt.title("Profanity Levels")

        file_name = indiv + "_BoxProfanity.png"
        out_path = os.path.join(base_outdir, file_name)
        plt.savefig(out_path, bbox_inches='tight')

def calcToxicityOverTime(df, cancel_date, indiv, base_outdir):
    '''
    creates box plots and line graphs showing how toxicity levels change over time

    '''
    # CLEAN DATAFRAME
    inital_df = df[df['toxicity'] != 1000] 
    inital_df = df[df['severe_toxicity'] != 1000]
    inital_df = df[df['insult'] != 1000]
    inital_df = df[df['profanity'] != 1000]

    line_df = inital_df.copy()
    line_df['created_at'] = line_df['created_at'].apply(
            lambda x: count_days(x, cancel_date)).dt.days
    groupedUsers = line_df[['created_at', 'toxicity', 'severe_toxicity', 
        'insult', 'profanity']].groupby(by='created_at')

    # creates and saves line graphs 
    plt.clf()
    createToxicityLines(groupedUsers, 'toxicity', indiv, base_outdir)
    plt.clf()
    createToxicityLines(groupedUsers, 'severe_toxicity', indiv, base_outdir)
    plt.clf()
    createToxicityLines(groupedUsers, 'insult', indiv, base_outdir)
    plt.clf()
    createToxicityLines(groupedUsers, 'profanity', indiv, base_outdir)

def create_textblob_plot(data, target, outdir):
    '''
    produces line plot tracking polarity of tweets relating to
    an individual before and after a controvery date for TextBlob
    '''
    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['sentiment polarity']

    plt.figure(figsize = (10,5)) # plot size
    sns.lineplot(data=pol_mean_daily)
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel("Polarity")
    plt.title("Mean Twitter Polarity of " + target + " Before and After Controversy")
    plt.axvline(0, 0.04, 0.99,color="red")
    png_file_name = target + "_textblob_polarity1.png"
    out_path_png = os.path.join(outdir, png_file_name)
    plt.savefig(out_path_png,dpi=300, bbox_inches = "tight")
    plt.close()

def plotPolarity(data, target, outdir):
    '''
    produces line plot tracking polarity of tweets relating to
    an individual before and after a controvery date for Vader
    '''
    pol_mean_daily = data.groupby("Days Before & After Controversy").mean()['Compound']

    plt.figure(figsize = (10,5)) # plot size 
    sns.lineplot(data=pol_mean_daily)
    plt.xlabel('# Days Before and After Cancellation')
    plt.ylabel("Polarity")
    plt.title("Mean Twitter Polarity of " + target + " Before and After Controversy")
    plt.axvline(0, 0.04, 0.99,color="red")
    png_file_name = target + "_vader_polarity1.png"
    out_path_png = os.path.join(outdir, png_file_name)
    plt.savefig(out_path_png,dpi=300, bbox_inches = "tight")
    plt.close()

def cleanData(df):
    '''
    remove tweets that start w/ RT (as it usually indicates that the tweet
    contains copypasta text and/or is retweeted from someone else)
    '''
    data = df.copy()
    data['boolean'] = data['text'].apply(lambda x: True if x[:2] == 'RT' else False)
    new_df = data[data['boolean'] == False].reset_index(drop=True)
    new_df = new_df.drop(columns=['boolean'])

    file_path = ""
    new_df.to_csv(file_path, index=False)

def calculate_stats(data_dict, test=False):
    if test:
        base_outdir = ".//data/test/test_out"
        tempdir = ".//data/test/test_temp/"
    else:
        base_outdir = ".//data/out/"
        tempdir = ".//data/temp/"

    artist_names = list(data_dict.keys())

    for indiv in artist_names:
        toxicity_data = data_dict[indiv][0]
        # polarity_data = data_dict[indiv][1]
        # vader_data = data_dict[indiv][2]
        cancel_date = data_dict[indiv][1]

        toxicity_df = convert_dates(toxicity_data)
        
        # create csvs out of data
        userActivity_df = user_activity_levels(toxicity_df, indiv, cancel_date, tempdir)
        # counts number of tweets before and after cancellation 
        totalTweets = numOfTweets(toxicity_df, cancel_date)
        out_file_name = indiv + "_numOfTweetsBefAft.csv"

        out_path = os.path.join(base_outdir, out_file_name)
        totalTweets.to_csv(out_path)
        # create graphs + save as pngs
        plt.clf()
        create_userActivity_graph(userActivity_df, indiv, base_outdir)
        plt.clf()

        # generates visualizations from data generated by toxicity script
        calcToxicityOverTime(toxicity_df, cancel_date, indiv, base_outdir)

        # generates visualizations from data generated by textblob polarity script
        # create_textblob_plot(polarity_data, indiv, base_outdir)
        # plt.clf()
        
        # generates visualizations from data generated by vader script
        # plotPolarity(vader_data, indiv, base_outdir)
        # plt.clf()

    