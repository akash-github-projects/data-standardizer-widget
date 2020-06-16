# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 07:10:08 2020
Project : AnalyTechs
@author: Akash Gupta
"""

import logging
import warnings

import pandas as pd
from sklearn.preprocessing import (MinMaxScaler, StandardScaler, MaxAbsScaler,
                                   RobustScaler, QuantileTransformer, PowerTransformer)

# setting up the logging module
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.INFO)

error_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(error_format)

logger.addHandler(file_handler)

warnings.filterwarnings('ignore')


class ClsParameterException(Exception):
    "Custom Erros"


class ClsDataStandardizer:
    """
    Description:
        Class to standardize or normalize data by various scalers

    Usage:
        \\Importing the file into the code
            from Widget_Data_Standardizer import data_standardizer

        \\Creating an object x of the class
            x = data_standardizer(df_data, cols, round_val = 2)

        \\For normalizing data by MinMax Scaler
            df_min_max = x.apply_min_max_scaler(min = 0, max =10)
            Argument:
                min: minimum value to be referred for normalization (default value = 0)
                max: maximum value to be referred for normalization (default value = 1)

        \\For standardizing data by Standard Scaler
            df_min_max = x.apply_standard_scaler()

        \\For standardizing data by MaxAbs Scaler
            df_min_max = x.apply_max_abs_scaler()

    Arguments:
        df_data      : A pandas dataframe containing the data
        cols         : A list of strings containing all the attributes for standardization
        round_val    : An Integer value for rounding the float values to specific decimal places (default value =3)

    Returns:
        Returns dataframes with standardized or normalized data

    """

    def __init__(self, df_data, columns=None, round_val=3):

        if not isinstance(df_data, pd.DataFrame):
            raise ClsParameterException('Type Error: df_data but be a pandas df ')

        if columns is None:
            # sys.exit('No columns list passed')
            raise ClsParameterException('No columns list passed')

        self.cols = columns

        if len(df_data) == 0:
            # sys.exit('The passed dataframe is empty')
            raise ClsParameterException('The passed dataframe is empty')
        if len(self.cols) == 0:
            # sys.exit('The passed columns list is empty')
            raise ClsParameterException('The passed columns list is empty')

        self.df_data = df_data
        self.df_standardize = df_data
        self.round_val = round_val
        #  getting numerical columns
        self.num_cols = self.df_data[self.cols]._get_numeric_data().columns
        # getting categorical columns
        self.categorical_cols = list(set(self.cols) - set(self.num_cols))
        # setting the post fix of the scaled columns
        self.postfix = '_minmax_scaled'

        if len(self.categorical_cols) > 0:
            print(self.categorical_cols, 'is/are categorical features and cannot be standardized')

    def apply_min_max_scaler(self, min_=0, max_=1):
        """
        Apply min max scaler to the input dataset
        :param min_: min value
        :param max_: max value
        :return: object of the same function
        """

        if not isinstance(min_, int) and not isinstance(max_, int):
            raise ClsParameterException('Type Error: min and max must be integers')

        # updating the post fix
        self.postfix = '_minmax_scaled'

        scaling = MinMaxScaler(feature_range=(min_, max_))
        #       getting a normalized dataframe by min_max_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)
        #       appending the normalized dataframe in the passed dataframe
        return self

    def apply_standard_scaler(self):
        """
        apply standard scaler on the dataset
        :return: object of the same function
        """

        # updating the post fix
        self.postfix = '_standard_scaled'

        scaling = StandardScaler()
        #       getting a standardized dataframe by standard_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)
        return self

    def apply_max_abs_scaler(self):
        """
        Apply min max abs scaler to the input dataset
        :return: object of the same function
        """

        # updating the post fix
        self.postfix = '_max_abs_scaled'

        scaling = MaxAbsScaler()
        #       getting a standardized dataframe by max_abs_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)

        return self

    def apply_robust_scalar(self, quantile_range=(50, 75)):
        """
        Apply robust scaler to the input dataset
        :param quantile_range: tuple with contains the max and the min value
        :return: object of the same function
        """

        self.postfix = '_robust_scaled'

        scaling = RobustScaler(quantile_range=quantile_range)
        #       getting a standardized dataframe by apply_robust_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)

        return self

    def apply_quantile_scalar(self, distribution='normal'):
        """
        Apply quantile scaler to the input dataset
        :param distribution: it can be normal or uniform
        :return: object of the same function
        """

        if distribution not in ['normal', 'uniform']:
            raise ClsParameterException('Value Error - distribution can only be normal or uniform')

        self.postfix = '_quantile_scaled'

        scaling = QuantileTransformer(output_distribution=distribution)
        #       getting a standardized dataframe by apply_robust_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)
        return self

    def apply_power_scaler(self):
        """
        Apply power scaler to the input dataset
        :return: object of the same function
        """

        self.postfix = '_power_scaled'

        scaling = PowerTransformer()
        #       getting a standardized dataframe by apply_robust_scaler
        self.df_standardize = pd.DataFrame(scaling.fit_transform(self.df_data[self.num_cols]),
                                           columns=self.num_cols + self.postfix).round(self.round_val)
        return self

    def add_column_to_data(self, change=0):
        """
        To change the input dataset with the standardized column
        :param change: Boolean True or False
        :return: changes dataframe with standardized column
        """

        #  appending the standardized dataframe in the passed dataframe
        for column in self.df_standardize:
            self.df_data[column] = self.df_standardize[column]
        if change:
            return self
        return self.df_data

    def apply_all_scaler(self):
        """
        Applies all the scaler to the dataframe on the selected columns
        :return: changed dataframe with standardized column
        """
        return self.apply_min_max_scaler().add_column_to_data(change=1) \
            .apply_max_abs_scaler().add_column_to_data(change=1). \
            apply_standard_scaler().add_column_to_data(change=1). \
            apply_robust_scalar().add_column_to_data(change=1). \
            apply_power_scaler().add_column_to_data(change=1). \
            apply_quantile_scalar().add_column_to_data()

    def make_column_pair(self):
        """

        :return: Returns the column pair
        """
        paired_columns = []
        for column in self.num_cols:
            paired_columns.append([column, str(column) + str(self.postfix)])

        return paired_columns

    def get_column_pair(self, col):
        """

        :param col: col which pair is required
        :return: paired col
        """
        return col + self.postfix
