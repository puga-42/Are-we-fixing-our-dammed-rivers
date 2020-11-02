import numpy as np
import pandas as pd


def drop_nans(df, ax, how):
    '''
        Drops rows or collumns from a that contain nans
        
        ARGS:
            df - pandas dataframe
            ax - 0 for row, 1 for column
            how - 'all' if enire ax is nans, 'any' if less than all
        Return:
            df - reduced dataframe
    '''
    df = df.dropna(axis=ax, how=how)
    return df

def get_impaired_waters_types(df, col):
    '''
        fill's NaN values in the 'Water Body Type' column
        with 'Null', then gets all the different water body 
        types along with their counts on the 303d list

        ARGS:
            df - impaired waters dataframe
            col - 'Water Body Types' column

        Return:
            list - [list_of_water_bodies, count_of_water_bodies]
    '''
    body_dict = {}
    df[col] = df[col].fillna('Null')

    for body in df[col]:
        if body in body_dict:
            body_dict[body] += 1
        else:
            body_dict[body] = 1
    
    body_list = []
    amount_list = []
    for k, v in body_dict.items():
        body_list.append(k)
        amount_list.append(int(v))
    
    return [body_list, amount_list]



def fill_nans(df, col, replace_with):
    '''
        replace NaNs with specified values

        ARGS: 
            df - dataframe
            col - column with nans
            replace_with - value to insert in place of NaN

        Return:
            none
    '''

    d = {}
    df['col'] = df['col'].fillna(replace_with)


def filter(df, col, text):
    '''
        ARGS:
            df - dataframe
            col - column of dataframe
            text - exact string or int to remove if it appears in col
        Return:
            df - updated df
    '''

    df = df.loc[df[col] != text]
    return df

def clean_waters_data(waters):
    '''
        cleans waters data. drops nans, removes all entries that 
        aren't Rivers or Streams, converts all strings to lowercase, converts
        numeric values to ints, reindexes df.

        ARGS:
            waters - waters dataframe
        
        Return:
            rivers - cleaned rivers dataframe
    '''
    
    waters = waters.dropna(axis=0, how='all')
    rivers = waters.loc[waters['WATER BODY TYPE'] == 'River & Stream']
    rivers = rivers[['Region', 'Water Body Name', 'POLLUTANT']]
    rivers['Water Body Name'] = rivers['Water Body Name'].str.lower()

    to_numeric(rivers, ['Region'])
    rivers.index = np.arange(0, len(rivers))

    return rivers



def clean_dams(dams):

    '''
        cleans dams data. 


    '''
    dams = dams.rename(columns={'RIVER': 'River', 'PRIVATE_DAM': 'Private Dam'})

    dams = dams[['River', 'Private Dam']]
    dams = dams[dams['River'].notna()]
    dams['River'] = dams['River'].str.lower()
    dams = filter(dams, 'River', 'offstream')
    dams = filter(dams, 'River', 'y')
    dams = filter(dams, 'River', '.')
    dams = filter(dams, 'River', 3)

    dams = dams.drop_duplicates(subset='River', keep="first")

    return dams


def reset_index(df):

    '''
        reindexes dataframe with ints starting at 0.

        ARGS:
            df - dataframe to reindex
        Returns:
            none

    '''
    df.index = np.arange(0, len(df))

def to_numeric(df, cols):

    '''
    converts column to ints
    
    ARGS:
        df - dataframe
        col - column to change to ints

    Returns:
        None

    '''
    for col in cols:
        df[col] = df[col].apply(lambda x: pd.to_numeric(x, errors='coerce'))

    
def condense(df):
    '''
        Makes new dataframe column, 'All Pollutants'. Combines all pollutants for each river into
        one column.

        ARGS:
            df - waters dataframe
        Returns:
            dataframe - condensed df
    '''

    df['All Pollutants'] = df[[
    'Water Body Name',
    'POLLUTANT']].groupby('Water Body Name')['POLLUTANT'].transform(lambda x: ', '.join(x))

    df = df[['Water Body Name', 'All Pollutants' , 'Region']].drop_duplicates()
    return df


def add_col_num_pollutants(df):
    '''
        Adds new dataframe column, 'Number of Pollutants', which is a count
        of all pollutants in, 'All Pollutants'

        ARGS:
            df - waters df
        Returns:
            df - updated df
    '''

    df['Number of Pollutants'] = 0
    for i in range (df['All Pollutants'].count()):
        pollutant_list = df['All Pollutants'][i].split(', ')
        pollutant_list = list(dict.fromkeys(pollutant_list))
        df['All Pollutants'][i] = pollutant_list
        df['Number of Pollutants'][i] = len(pollutant_list)

    return df


def merge_dfs(df1, df2, left, right):
    '''
        merges two dataframes

        ARGS:
            df1, df2 - dataframe
            left - column to join on df1
            right - column to join on df2
        Returns:
            df - merged dataframe
    '''

    df1 = df1.set_index('Water Body Name', drop=False)
    df1 = df1.rename(columns={'Water Body Name': 'River'})

    for impaired_river in df1['River']:
    
        for dammed_river in df2['River']:
            if dammed_river in impaired_river:
                df1['River'].loc[df1['River'] == impaired_river] = dammed_river
                impaired_river = dammed_river
                break

    df = df2.groupby(['River'], sort=False)['Private Dam'].apply(lambda x: ','.join(x.astype(str)))
    df = df1.merge(df2, how='left', left_on=left, right_on=right)
    
    return df



def bootstrap_sample_means(data, n_bootstrap_samples=10000):
    bootstrap_sample_means = []
    for i in range(n_bootstrap_samples):
        bootstrap_sample = np.random.choice(data, size=300, replace=True)  ##changed from size=len(data)
        bootstrap_sample_means.append(np.mean(bootstrap_sample))
    
    return bootstrap_sample_means


def combine_dicts(d1, d2):
    '''
        combine keys of two dictionaries

    ARGS:
        d1, d2 - dictionaries
    Returns:
        d3 - dictionary with keys comprising all of d1 and d2
    '''
    d3 = d1
    for k, v in d2.items():
        if k not in d3:
            d3[k] = v
    return d3

def solvability(most_potent_dict, treatable):
    '''
        returns a list: [number of pollutants solvable with TMDLS, 
        number of pollutants not solvable with TMDLS]

        ARGS:
            most_potent_dict - dictionary with keys = pollutants, values = counts
            treatable - dictionary with values = pollutants, values = 'Yes" or 'No'

        Returns:
            list - [number of pollutants solvable, number not solvable]
    '''

    solvable = 0
    unsolvable = 0
    for k, v in most_potent_dict.items():
        if treatable[k] == 'Yes':
            solvable += v
        else:
            unsolvable += v
    return [solvable, unsolvable]


def get_pollutant_dict(df):
    '''
        Compiles a dictionary from df. Keys = pollutants, 
        values = counts.

        ARGS:
            df - dataframe
        Returns:
            dict - keys = pollutants, values = counts
    '''

    pollutant_dict = {}
    for pol in df['All Pollutants']:
        for pollutant in pol:
            if pollutant in pollutant_dict:
                pollutant_dict[pollutant] += 1
            else:
                pollutant_dict[pollutant] = 1
            
    return pollutant_dict


def get_first_n(d, n):
    '''
        Returns the top n values of a dictionary

        ARGS:
            d - dictionary
            n - number of items to return

        Return:
            dictionary with n entries
    '''
    top_n = {}
    for i in range(n):
        d_copy = d
        largest_key = max(d_copy, key=d_copy.get)
        top_n[largest_key] = d_copy[largest_key]
        del d_copy[largest_key]
    return top_n

