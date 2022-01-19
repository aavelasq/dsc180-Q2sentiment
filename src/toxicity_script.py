import pandas as pd 
import apikeys # apikey file
from googleapiclient import discovery
import time

tempdir = ".//data/temp/"
googleAPIKEY = apikeys.api_keys['googleKey']

def toxicityFunc(data, target):
    '''
    calculates the toxicity, severe toxicity, insult, and profanity
    probabilities using Google's Perspective API for each tweet
    in a dataset
    '''
    client = discovery.build(
            "commentanalyzer",
            "v1alpha1",
            developerKey=googleAPIKEY,
            discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
            static_discovery=False,
        )

    tweet_count = 0 
    main_df = pd.DataFrame()
    tweet_dict = {}

    for index, row in data.iterrows(): 
        tweet_text = row['text']
        tweet_date = row['created_at']
        tweet_id = row['id']

        if tweet_text in tweet_dict.keys():
            # if there are tweets with the same text/copypasta tweets
            # thus unnecessary to make a completely new request
            toxicity_val = tweet_dict[tweet_text][0]
            severe_val = tweet_dict[tweet_text][1]
            insult_val = tweet_dict[tweet_text][2]
            profanity_val = tweet_dict[tweet_text][3]
        else: 
            # MAKES REQUEST TO API 
            try: 
                analyze_request = {
                        'comment': {'text': tweet_text},
                        'requestedAttributes': {'TOXICITY': {}, 
                        'SEVERE_TOXICITY': {}, 'INSULT': {}, 'PROFANITY': {}}
                    }
                
                response = client.comments().analyze(body=analyze_request).execute()
                toxicity_val = response['attributeScores']['TOXICITY']['summaryScore']['value']
                severe_val = response['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
                insult_val = response['attributeScores']['INSULT']['summaryScore']['value']
                profanity_val = response['attributeScores']['PROFANITY']['summaryScore']['value']
            except: # if language is not english as recognized by api
                toxicity_val = 1000
                severe_val = 1000
                insult_val = 1000
                profanity_val = 1000

            # assign toxicity value to text in dictionary
            tweet_dict[tweet_text] = [toxicity_val, severe_val, insult_val, profanity_val]
            time.sleep(0.0001)

        # print statements
        # print("index: " + str(index))
        # tweet_count += 1
        # print(tweet_count)

        # add to main dataframe 
        temp_df = pd.DataFrame({'text': [tweet_text], 'created_at': [tweet_date], 'id': [tweet_id],
        'toxicity': [toxicity_val], 'severe_toxicity': [severe_val], 
        'insult': [insult_val], 'profanity': [profanity_val]})
        main_df = pd.concat([main_df, temp_df]) # adds on to existing dataframe of tweets

        file_name = tempdir + target + '_toxicVals2.csv'
        main_df.to_csv(file_name, index=False)