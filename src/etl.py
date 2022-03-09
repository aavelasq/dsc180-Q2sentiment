import pandas as pd
import datetime

# CHANGE DATE DEPENDING ON INDIVIDUAL 
maleKpop_cancel_date = datetime.datetime(2021, 8, 24) # LUCAS
femaleKpop_cancel_date = datetime.datetime(2021, 10, 23) # GISELLE

maleHH_cancel_date = datetime.datetime(2021, 7, 25) # DABABY
femaleHH_cancel_date = datetime.datetime(2021, 9, 13) # NICKI

malePop_cancel_date = datetime.datetime(2021, 8, 28) # ZAYN
femalePop_cancel_date = datetime.datetime(2020, 5, 25) # DOJA CAT

# list of cancelled individuals 
male_kpop_list = ['JAEMIN', 'LUCAS']
female_kpop_list = ['GISELLE', 'RYUJIN']

male_hiphop_list = ['DABABY', 'LILBABY']
female_hiphop_list = ['NICKI', 'SAWEETIE']

male_pop_list = ['ZAYN', 'HARRY']
female_pop_list = ['DOJA', 'ADELE']

def data_helper_func(file_dir, input_list, output_dict, cancel_date):
    '''
    helper function for import_main_data
    imports toxicity, vader, polarity csv files 
    '''
    for indiv in input_list:
        toxic_file = file_dir + indiv + '_toxicVals.csv'
        toxic_df = pd.read_csv(toxic_file)

        # polarity_file = file_dir + indiv + '_meanPolarity.csv'
        # polarity_df = pd.read_csv(polarity_file)

        # vader_file = file_dir + indiv + '_vaderPolarity.csv'
        # vader_df = pd.read_csv(vader_file)
        
        output_dict[indiv] = [toxic_df, cancel_date]

    return output_dict

def tweet_helper_func(base_dir, input_list, cancel_date):
    '''
    helper function for import_acc_data
    imports tweets from individual's account 6 months before and after cancellation
    '''
    output_dict = {}

    for indiv in input_list:
        input_path = base_dir + indiv + "_tweets.csv"
        df = pd.read_csv(input_path)
        output_dict[indiv] = [df, cancel_date]

    return output_dict

def import_acc_data(base_dir, test=False):
    '''
    imports data of tweets gathered from target individual's twitter acccounts
    ''' 
    # initalize variables
    male_kpop_dict = {}
    female_kpop_dict = {}
    male_hiphop_dict = {}
    female_hiphop_dict = {}
    male_pop_dict = {}
    female_pop_dict = {}

    cancel_date = datetime.datetime(2022, 2, 6)
    if test:
       maleKpop_cancel_date = cancel_date
       femaleKpop_cancel_date = cancel_date
       maleHH_cancel_date = cancel_date
       femaleHH_cancel_date = cancel_date
       malePop_cancel_date = cancel_date
       femalePop_cancel_date = cancel_date

    # kpop dicts 
    male_kpop_dict = tweet_helper_func(base_dir, male_kpop_list, maleKpop_cancel_date)
    female_kpop_dict = tweet_helper_func(base_dir, female_kpop_list, femaleKpop_cancel_date)

    male_hiphop_dict = tweet_helper_func(base_dir, male_hiphop_list, maleHH_cancel_date)
    female_hiphop_dict = tweet_helper_func(base_dir, female_hiphop_list, femaleHH_cancel_date)

    male_pop_dict = tweet_helper_func(base_dir, male_pop_list, malePop_cancel_date)
    female_pop_dict = tweet_helper_func(base_dir, female_pop_list, femalePop_cancel_date)

    return [male_kpop_dict, female_kpop_dict, 
            male_hiphop_dict, female_hiphop_dict, 
            male_pop_dict, female_pop_dict]

def import_main_data(genre1_dir, genre2_dir, genre3_dir, test=False):
    '''
    main func used for data target
    '''
    # initalize variables
    male_kpop_dict = {}
    female_kpop_dict = {}
    male_hiphop_dict = {}
    female_hiphop_dict = {}
    male_pop_dict = {}
    female_pop_dict = {}

    # test cancel date
    cancel_date = datetime.datetime(2022, 2, 6)
    if test:
        # kpop dicts 
        male_kpop_dict = data_helper_func(genre1_dir, male_kpop_list, 
            male_kpop_dict, cancel_date)
        female_kpop_dict = data_helper_func(genre1_dir, female_kpop_list, 
            female_kpop_dict, cancel_date)

        # hiphop dicts
        male_hiphop_dict = data_helper_func(genre2_dir, male_hiphop_list, 
            male_hiphop_dict, cancel_date)
        female_hiphop_dict = data_helper_func(genre2_dir, female_hiphop_list, 
            female_hiphop_dict, cancel_date) 
        
        # pop dicts
        male_pop_dict = data_helper_func(genre3_dir, male_pop_list, 
            male_pop_dict, cancel_date)
        female_pop_dict = data_helper_func(genre3_dir, female_pop_list, 
            female_pop_dict, cancel_date) 

    else:
        # kpop dicts 
        male_kpop_dict = data_helper_func(genre1_dir, male_kpop_list, 
            male_kpop_dict, maleKpop_cancel_date)
        female_kpop_dict = data_helper_func(genre1_dir, female_kpop_list, 
            female_kpop_dict, femaleKpop_cancel_date)

        # hiphop dicts
        male_hiphop_dict = data_helper_func(genre2_dir, male_hiphop_list, 
            male_hiphop_dict, maleHH_cancel_date)
        female_hiphop_dict = data_helper_func(genre2_dir, female_hiphop_list, 
            female_hiphop_dict, femaleHH_cancel_date) 
        
        # pop dicts
        male_pop_dict = data_helper_func(genre3_dir, male_pop_list, 
            male_pop_dict, malePop_cancel_date)
        female_pop_dict = data_helper_func(genre3_dir, female_pop_list, 
            female_pop_dict, femalePop_cancel_date) 

    return [male_kpop_dict, female_kpop_dict, 
            male_hiphop_dict, female_hiphop_dict, 
            male_pop_dict, female_pop_dict]
