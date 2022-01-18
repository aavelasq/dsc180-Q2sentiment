# imports
import twitterkeys # apikeys file
import pandas as pd
import requests
import datetime
from datetime import timedelta
import time
from os import listdir
from os.path import isfile, join

bearer_token = twitterkeys.apikeys['bearer_token']

search_url = "https://api.twitter.com/2/tweets/search/all"
# save tweets dataframe to this location
out_path = ".//data/raw/"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    '''
    helper function to process requests to Twitter API
    '''
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def twitter_scraper():
    '''
    main scraper function to process queries which gets Tweets from Twitter API
    '''
    df = pd.DataFrame() # initializes empty dataframe 
    tweet_count = 0 # initializes tweet count 
    next_token = "" # initializes next token
    num_requests = 0 # intializes the number of requests made 
 
    date = datetime.datetime(2021, 4, 23, 0, 0, 0) # start date
    # final_date = date + datetime.timedelta(days=323) # end date
    # stop at jan. 14 2022
    final_date = datetime.datetime(2022, 1, 14, 0, 0, 0)
    
    while date != final_date:
        start_time = datetime.datetime.strftime(date, r"%Y-%m-%dT%H:%M:%SZ")
        end_date = date + datetime.timedelta(days=1) 
        end_time = datetime.datetime.strftime(end_date, r"%Y-%m-%dT%H:%M:%SZ")

        # PUT QUERY HERE 
        if next_token == "": 
            query_params = {'query': 'QUERY lang:en -has:links -is:retweet -is:reply', 
                            'max_results': '100', 
                            'start_time': start_time, 
                            'end_time': end_time, 
                            'tweet.fields': 'created_at,author_id'}
        else: 
            query_params = {'query': 'QUERY lang:en -has:links -is:retweet -is:reply', 
                        'max_results': '100', 
                        'start_time': start_time, 
                        'end_time': end_time, 
                        'tweet.fields': 'created_at,author_id',
                        'next_token': next_token}

        json_response = connect_to_endpoint(search_url, query_params)
        print(json_response)
        num_requests += 1 # increment num of requests by 1 
        print("Number of Requests: " + str(num_requests))

        if json_response['meta']['result_count'] != 0:
            df1 = pd.DataFrame(json_response['data'])
            df = pd.concat([df, df1]) # adds on to existing dataframe of tweets
            
            tweet_count += len(df1)
            print('Tweets Gathered:', str(len(df)))

            # CHANGE FILE NAME HERE 
            df.to_csv(out_path, index = False) # converts df to csv

        if 'next_token' in json_response['meta']: 
            # on next loop, will use the same query as the prev loop but goes
            # to the next page of prev query
            next_token = json_response['meta']['next_token']
        else:
            # goes on to next query
            date += timedelta(days=1) # increases time by x hours
            next_token = ""

        time.sleep(5) # num of seconds between each query

        print()

def combine_raw_data():
    '''
    combines all datasets contained in raw data directory 
    '''
    file_names = [f for f in listdir("./data/raw/") if isfile(join("./data/raw/", f))]
    df_list = []

    for file in file_names:
        file_str = "./data/raw/" + file
        df = pd.read_csv(file_str)
        df_list.append(df)
    
    final_df = pd.concat(df_list).drop_duplicates().reset_index(drop=True)
    final_df = final_df.sort_values(by=['created_at'], ascending=True).reset_index(drop=True)
    final_df.to_csv(".//data/raw/", index=False)
    print(len(final_df))

def main():
    twitter_scraper() # runs twitter scraper func 
    # combine_raw_data() # combines raw data into one dataset

if __name__ == "__main__":
    main()