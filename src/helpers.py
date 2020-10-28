import numpy as np
import pandas as pd

def to_numeric(df, cols):
    for col in cols:
        df[col] = df[col].apply(lambda x: pd.to_numeric(x, errors='coerce'))

def to_str(df, cols):
    for col in cols:
        df[col] = df[col].apply(lambda x: pd.to_string(x, errors='coerce'))
        




def get_impaired_dams(dams, impaired_waters):
    impaired_dict = {}
    for dam in dams['RIVER']:
        for river in impaired_waters['Water Body Name']:
            if river.str.contains('|'.join(dam)) == True:
                impaired_dict[dam] = river

    
    return impaired_dict




#pd.DataFrame.from_dict(data, orient='index',
#                       columns=['A', 'B', 'C', 'D'])

#dams_data['impaired'] = [True if ]
#searchfor = dams_data['RIVER']
#impaired_rivers['Water Body Name'][26].str.contains('|'.join(dams_data['RIVER'][100]))
#s = impaired_rivers['Water Body Name']

def the_dammed_and_impaired(dams, impaired_waters):

    ##how to find dammed impaired rivers?
    #1. If 'dam' in river's name
    #2. If 'dam' construction in possible causes
    #3. If dams_data.RIVER in impaired_rivers.name & state in states in region