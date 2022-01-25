import pandas as pd

def import_test_data(test_dir, file_dir):
    '''
    used for test target
    '''
    df = pd.read_csv(test_dir)
    return df

def import_data(test_dir, file_dir):
    '''
    used for data target
    '''
    df = pd.read_csv(file_dir)
    return df