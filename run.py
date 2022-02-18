import sys
import datetime
import pandas as pd
import json

sys.path.insert(0, 'src') # add src to paths

import etl
from eda import calculate_stats
from preprocessing import calculate_avgs
import parasocial
from visuals import create_visuals
# from toxicity_script import toxicityFunc
# from vader_script import polarityFunc
# from polarity_script import calc_textblob_polarity

# CHANGE DATE DEPENDING ON INDIVIDUAL
cancellation_date = datetime.datetime(2021, 9, 15)

def main(targets):
    # data_config = json.load(open('config/data-params.json'))

    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        # list of dicts for each genre divided by gender containing datasets 
        # aka two datasets per genre for male + female individuals
        # data generated from toxicity, polarity, and vader scripts
        data_list = etl.import_main_data(**data_cfg)

        tweet_list = etl.import_acc_data("./data/raw/")

        # for running API scripts
        # data = pd.read_csv(".//data/raw/Saweetie_tweets.csv")

    if 'eda' in targets:
        # data_list consists of dataframes for each gender per genre
        for data_dict in data_list:
            calculate_stats(data_dict)
        # calculate_stats(data)

    if 'preprocessing' in targets:
        with open('config/preprocessing-params.json') as fh:
            preproc_cfg = json.load(fh)

        for data_dict in data_list:
            calculate_avgs(data_dict, **preproc_cfg)

    if "parasocial" in targets:
        parasocial.create_parasocial_dfs("./data/temp/", tweet_list, data_list)
        
    if "visuals" in targets:
        with open('config/visuals-params.json') as fh:
            visual_cfg = json.load(fh)

        create_visuals(**visual_cfg)

    # UNCOMMENT IF RUNNING DATA ON API SCRIPTS
    # if 'toxicity' in targets:
    #     '''
    #     calculates toxicity sentiment using Google Perspective API
    #     '''
    #     # 2nd parameter: name of cancelled individual
    #     toxicityFunc(data, "name")

    # if 'polarity' in targets:
    #     '''
    #     calculates polarity sentiment using TextBlob library
    #     '''
    #     # 2nd parameter: name of cancelled individual
    #     calc_textblob_polarity(data, "name", cancellation_date)

    # if 'vader' in targets:
    #     '''
    #     calculates compound polarity using Vader library 
    #     '''
    #     # 2nd parameter: name of cancelled individual
    #     polarityFunc(data, "name", cancellation_date)

    if 'test' in targets:
        with open('config/test-params.json') as fh:
            data_cfg = json.load(fh)

        data_list = etl.import_test_data(**data_cfg)

        test_data_dict = {"test": data_list}

        # rq 1 function 
        calculate_stats(test_data_dict, test=True)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)

