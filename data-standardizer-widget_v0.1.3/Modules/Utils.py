# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 12:10:57 2020

@author: ar23102
"""
import pandas as pd

def _load_data(absolute_path, type_of_file='csv'):
    '''Loads data into a pandas Dataframe
    
    Parameters
    ----------
    absolute_path
        Absolute path of the file you want to load
        
    type_of_file
        Format of the file i.e. if the file is csv or excel or pickle
        
    Returns
    -------
    df_data
        Pandas dataframe of the loaded data
    '''
    if type_of_file == 'csv':
        df_data = pd.read_csv(absolute_path)
    elif type_of_file == 'xlsx':
        df_data = pd.read_excel(absolute_path)
    elif type_of_file == 'pickle':
        df_data = pd.read_pickle(absolute_path)
    return df_data

