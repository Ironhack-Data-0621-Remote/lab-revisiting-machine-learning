# data pre-processing functions incl. cleaning, eda, feature engineering

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import datetime
import math
import random
import re


# function to standardize column names
# inputs: df
# outputs: df
def clean_headers(df):
    df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_')
    return df


# function to replace strings in a df
# inputs: df, dict with column names as keys and list(2) as values, value 0 - regex replace pattern, value 1 - replacement str
# outputs: df
def clean_data(df, cleaner):
    for column in cleaner:
        print('Cleaning', column)
        for x in range(len(df[column])):
            df[column].iloc[x] = re.sub(cleaner[column][0], cleaner[column][1], df[column].iloc[x])
    print('Done')
    return df


# function to create a df with an overview of the amount of NaNs, empty fields, zeros and negative values in all columns of a df
# option to only show columns with amount of unwelcome values above a chosen threshold
# inputs: df, threshold percentage (float), bool. ind. to exclude negative numbers from the threshold
# outputs: overview df, list of columns shown
def value_overview(df, limit=0, neg_allowed=False):
    # creating columns for data type, no of unique values, NaNs
    df_dtypes = pd.DataFrame(df.dtypes, columns=['type'])
    no_uniques = pd.DataFrame(df.nunique(), columns=['unique values'])
    nulls = pd.DataFrame(df.isna().sum(), columns=['NaN'])
    nulls_percent = pd.DataFrame(round(df.isna().sum()*100/len(df), 2), columns=['NaN %'])

    # lists for of no of zeros, empty cells, neg. values 
    zeros = [len(df[df[column] == 0]) if df_dtypes['type'].loc[column] != 'object' else 0 for column in df.columns]
    negative_values = [len(df[df[column] < 0]) if df_dtypes['type'].loc[column] != 'object' else 0 for column in df.columns]

    emptys_1 = [len(df[df[column] == '']) for column in df.columns]
    emptys_2 = [len(df[df[column] == ' ']) for column in df.columns]
    emptys = [(emptys_1[i] + emptys_2[i]) for i in range(len(emptys_1))]

    zeros_percent, negative_percent, emptys_percent = [], [], []

    zeros_percent = [round(zeros[j]*100/len(df), 2) for j in range(len(zeros))]
    negative_percent = [round(negative_values[j]*100/len(df), 2) for j in range(len(negative_values))]
    emptys_percent = [round(emptys[j]*100/len(df), 2) for j in range(len(emptys))]

    # df for of zeros, empty cells, neg. values 
    special_values = pd.DataFrame({'empty': emptys, 'empty %': emptys_percent, 'zeros': zeros, 'zeros %': zeros_percent, 'negative': negative_values, 'negative %': negative_percent})
    special_values.index = df_dtypes.index
    
    # concat
    overview = pd.concat([df_dtypes, no_uniques, nulls, nulls_percent, special_values], axis=1)

    # option to filter overview with threshold value
    if limit != 0:
        overview['removable %'] = overview['NaN %']
    
        for x in overview['removable %']:
            if neg_allowed == False:
                overview['removable %'] = overview['NaN %'] + overview['empty %'] + overview['negative %']
            else:
                overview['removable %'] = overview['NaN %'] + overview['empty %']
    
        overview = overview[overview['removable %'] > limit].sort_values(by='removable %', ascending = False)
        print(len(overview), 'columns are missing at least', limit, '% of the data')
    
    return overview, list(overview.index)


# function to drop columns
# inputs: df, list of columns
# outputs: df
def drop_features(df, drop):
    df = df.drop(columns=drop)
    return df


