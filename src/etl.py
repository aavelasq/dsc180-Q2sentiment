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

male_hiphop_list = ['DABABY', 'LIL_BABY']
female_hiphop_list = ['NICKI_MINAJ', 'SAWEETIE']

male_pop_list = ['ZAYN', 'HARRY']
female_pop_list = ['DOJA', 'ADELE']

def import_test_data(toxicity, polarity,vader):
    '''
    used for test target
    '''
    cancel_date = datetime.datetime(2022, 2, 6)
    toxicity_df = pd.read_csv(toxicity)
    polarity_df = pd.read_csv(polarity)
    vader_df = pd.read_csv(vader)

    return [toxicity_df, polarity_df, vader_df, cancel_date]

def data_helper_func(file_dir, input_list, output_dict, cancel_date):
    for indiv in input_list:
        toxic_file = file_dir + indiv + '_toxicVals.csv'
        toxic_df = pd.read_csv(toxic_file)

        polarity_file = file_dir + indiv + '_meanPolarity.csv'
        polarity_df = pd.read_csv(polarity_file)

        vader_file = file_dir + indiv + '_vaderPolarity.csv'
        vader_df = pd.read_csv(vader_file)

        output_dict[indiv] = [toxic_df, polarity_df, vader_df, cancel_date]

    return output_dict

def import_data(test_dir, genre1_dir, genre2_dir, genre3_dir):
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
    # male_pop_dict = data_helper_func(genre3_dir, male_pop_list, 
    #     male_pop_dict, malePop_cancel_date)
    # female_pop_dict = data_helper_func(genre3_dir, female_pop_list, 
    #     female_pop_dict, femalePop_cancel_date) 

    return [male_kpop_dict, female_kpop_dict, 
            male_hiphop_dict, female_hiphop_dict]