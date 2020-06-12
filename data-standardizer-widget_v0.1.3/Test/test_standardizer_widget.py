import os
import sys
import unittest
import importlib
import sys
sys.path.append('..')

import pandas as pd

base_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir)

config_path = os.path.join(base_path, "config") + os.sep
log_path = os.path.join(base_path, "logs") + os.sep
backend_path = os.path.join(base_path, "backend") + os.sep
frontend_path = os.path.join(base_path, "Modules") + os.sep

sys.path.extend([config_path, log_path, backend_path, frontend_path])

Modules = importlib.import_module('Modules')

from Modules.Widget_Data_Standardizer import ClsDataStandardizer, ClsParameterException
from sklearn.preprocessing import (MinMaxScaler, StandardScaler, MaxAbsScaler,
                                   RobustScaler, QuantileTransformer, PowerTransformer)


class ClsDataStandardizerTest(unittest.TestCase):

    data = {
        'Name': ['One', 'Two', 'Three', 'Four', 'Five', 'Ash', 'Alcalinity of ash', 'Magnesium', 'Total phenols',
                 'Flavanoids', 'Nonflavanoid phenols', 'Proanthocyanins', 'Color intensity', 'Hue'],
        'Alcohol': [14.23, 13.2, 13.16, 14.37, 13.24, 14.2, 14.39, 14.06, 14.83, 13.86, 14.1, 14.12, 13.75, 14.75],
        'Malic Acid': [1.71, 1.78, 2.36, 1.95, 2.59, 1.76, 1.87, 2.15, 1.64, 1.35, 2.16, 1.48, 1.73, 1.73]
    }
    data_frame = pd.DataFrame(data)

    def test_object_column(self):
        self.assertRaises(ClsParameterException, ClsDataStandardizer, ClsDataStandardizerTest.data_frame)

    def test_object_data(self):
        empty_dataframe = pd.DataFrame()
        self.assertRaises(ClsParameterException, ClsDataStandardizer, empty_dataframe)

    def test_object_column2(self):
        self.assertRaises(ClsParameterException, ClsDataStandardizer, ClsDataStandardizerTest.data_frame, [])

    def test_min_max_scaler(self):

        scaling = MinMaxScaler(feature_range=(0, 1))

        # getting a normalized dataframe by min_max_scaler
        df_standardize = pd.DataFrame(scaling.fit_transform(ClsDataStandardizerTest.data_frame[['Alcohol']]),
                                      columns=['Alcohol_minmax_scaled']).round(3)
        # print(df_standardize.head())

        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])
        cls_std = std_obj.apply_min_max_scaler().df_standardize
        # print(cls_std.head())

        self.assertEqual(df_standardize.equals(cls_std), True)

    def test_standard_scaler(self):

        scaling = StandardScaler()

        # getting a normalized dataframe by min_max_scaler
        df_standardize = pd.DataFrame(scaling.fit_transform(ClsDataStandardizerTest.data_frame[['Alcohol']]),
                                      columns=['Alcohol_standard_scaled']).round(3)
        # print(df_standardize.head())

        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])
        cls_std = std_obj.apply_standard_scaler().df_standardize
        # print(cls_std.head())

        self.assertEqual(df_standardize.equals(cls_std), True)

    def test_robust_scaler(self):

        scaling = RobustScaler()

        # getting a normalized dataframe by min_max_scaler
        df_standardize = pd.DataFrame(scaling.fit_transform(ClsDataStandardizerTest.data_frame[['Alcohol']]),
                                      columns=['Alcohol_robust_scaled']).round(3)
        # print(df_standardize.head())

        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])
        cls_std = std_obj.apply_robust_scalar(quantile_range=(25.0, 75.0)).df_standardize
        # print(cls_std.head())

        self.assertEqual(df_standardize.equals(cls_std), True)

    def test_quantile_scaler(self):

        scaling = QuantileTransformer()

        # getting a normalized dataframe by min_max_scaler
        df_standardize = pd.DataFrame(scaling.fit_transform(ClsDataStandardizerTest.data_frame[['Alcohol']]),
                                      columns=['Alcohol_quantile_scaled']).round(3)
        # print(df_standardize.head())

        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])
        cls_std = std_obj.apply_quantile_scalar(distribution='uniform').df_standardize
        # print(cls_std.head())

        self.assertEqual(df_standardize.equals(cls_std), True)

    def test_power_scaler(self):

        scaling = PowerTransformer()

        # getting a normalized dataframe by min_max_scaler
        df_standardize = pd.DataFrame(scaling.fit_transform(ClsDataStandardizerTest.data_frame[['Alcohol']]),
                                      columns=['Alcohol_power_scaled']).round(3)
        # print(df_standardize.head())

        test_df = ClsDataStandardizerTest.data_frame

        for column in df_standardize:
            test_df[column] = df_standardize[column]

        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])
        cls_std = std_obj.apply_power_scaler().df_standardize

        new_cls_df = std_obj.apply_power_scaler().add_column_to_data()
        # print(cls_std.head())

        self.assertEqual(df_standardize.equals(cls_std), True)
        self.assertEqual(test_df.equals(new_cls_df), True)

    def test_column_pair(self):

        columns_pairs = [['Alcohol', 'Alcohol_power_scaled']]
        paired_column = 'Alcohol_power_scaled'

        # getting a normalized dataframe by min_max_scaler
        std_obj = ClsDataStandardizer(ClsDataStandardizerTest.data_frame, ['Alcohol'])

        new_std_obj = std_obj.apply_power_scaler().add_column_to_data(change=1)
        code_column_pair = new_std_obj.make_column_pair()

        self.assertListEqual(columns_pairs, code_column_pair)
        self.assertEqual(paired_column, new_std_obj.get_column_pair('Alcohol'))


if __name__ == '__main__':
    unittest.main()
