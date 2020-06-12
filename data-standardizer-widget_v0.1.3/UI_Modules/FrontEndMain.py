# -*- coding: utf-8 -*-
"""
Created on Wed April 13 07:10:08 2020
Project : AnalyTechs
@author: Akash Gupta
"""
import base64
import importlib
import io
import time
import logging
from datetime import datetime as dt

import boto3
import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, clear_output, Javascript
from Modules.Widget_Data_Standardizer import ClsDataStandardizer
from Modules.config import colors, types_, logs_file_name
from .styles import print2, print3, print4

UiConf = importlib.import_module('Modules.CommonElements')
logs = importlib.import_module('logs')
from logs import log_path

# setting up the logging module
logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(log_path + logs_file_name)
file_handler.setLevel(logging.INFO)

error_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(error_format)

logger.addHandler(file_handler)

# list of all the global functions
upload = widgets
global data_standardizer
global scaled_data
global analysis_df
global res
global s3_output
global path_output
global df_data
global s3_inp
global show_result
global error_widget

s3_output = widgets.Output()
path_output = widgets.Output()
error_widget = widgets.Output()
df_data = pd.DataFrame()

res = True
s3_inp = False
show_result = False


def fcnDataUploadAccordian():
    """
    This function is responsible for the upload of the data from the
    local file system or from the s3 bucket.
    :return: ui made from ipywidget
    """
    try:
        global upload
        global correlation_dropdowns
        global columns_multiselect
        global btn_generate_results
        global btn_data_upload
        global access_key
        global secret_key
        global df_data
        global choices
        global columns_multiselect
        global path_output
        global s3_inp
        global error_widget

        upload = widgets.FileUpload()

        upload1_label = widgets.HTML(
            value="<b><font color={}>Browse </b> (Required: To take samples from)".format(UiConf.text_font_style))

        data_button_grid = widgets.GridspecLayout(4, 8)
        data_button_grid[0, 0:3] = upload1_label
        data_button_grid[2, 0:3] = upload

        access_key = widgets.Text(value='', placeholder='', description='Access Key:')
        secret_key = widgets.Password(value='', placeholder='', description='Secret Key:')
        bucket_name = widgets.Text(value='', placeholder='', description='Bucket Name:', )
        file_location = widgets.Text(value='', placeholder='', description='File Location:', )
        file_name = widgets.Text(value='', placeholder='', description='File Name:', )
        region_name = widgets.Text(value='', placeholder='', description='Region Name:', )
        s3_button = widgets.Button(description="Get Data")
        s3_button.style.button_color = UiConf.inactive_button_color

        s3_grid = widgets.GridspecLayout(4, 3)
        s3_grid[0, 0] = access_key
        s3_grid[0, 1] = secret_key
        s3_grid[0, 2] = bucket_name
        s3_grid[1, 0] = file_location
        s3_grid[1, 1] = file_name
        s3_grid[1, 2] = region_name
        s3_grid[3, 0] = s3_button

        btn_data_summary = widgets.Button(
            description='DataSet Summary',
            disabled=False,
            button_style='',
            tooltip='Click me',
            icon='download',
            layout={'width': '200px'}
        )

        btn_data_summary.style.button_color = UiConf.inactive_button_color
        # emptying the data set
        df_data = pd.DataFrame()

        def fcnObserveUpload(b):
            if upload.data:
                with path_output:
                    path_output.clear_output()
                    [uploaded_file] = upload.value
                    if uploaded_file.split('.')[-1] == 'csv':
                        display(print4(
                            uploaded_file + " has been uploaded from Local System at " + str(
                                dt.now().replace(microsecond=0))))

                        time.sleep(0.5)

                        display(Javascript("IPython.notebook.scroll_to_cell(IPython.notebook.get_selected_index()+2)"))

                        display(Javascript(
                            'IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+2, '
                            'IPython.notebook.get_selected_index()+4)'))
                    else:
                        display(print2("Data cannot be read!"))

        upload.observe(fcnObserveUpload, names='value')

        def fcnUploadButtonClicked(b):
            global df_data
            global s3_inp
            Bucket_name = bucket_name.value
            file_S3_location = file_location.value
            File_name = file_name.value
            region = region_name.value

            with s3_output:
                s3_output.clear_output()
                display(print2("Retrieving data. . ."))
            try:
                df_data = fcnReadS3File(Bucket_name, file_S3_location, File_name, n_rows=None, header_=True,
                                        region_name=region)
            except:
                with s3_output:
                    s3_output.clear_output()
                    display(print2("Invalid details inserted, please check again"))
                    return

            s3_inp = True

            with s3_output:
                s3_output.clear_output()
                display(print3("Data Retrieved Successfully"))
            with path_output:
                path_output.clear_output()
                s3_inp = True
                display(print4(File_name + " has been read from S3 at " + str(dt.now().replace(microsecond=0))))

                time.sleep(0.5)

                display(Javascript("IPython.notebook.scroll_to_cell(IPython.notebook.get_selected_index()+2)"))

                display(Javascript(
                    'IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+2, '
                    'IPython.notebook.get_selected_index()+4)'))

        s3_button.on_click(fcnUploadButtonClicked)

        tab_nest = widgets.Tab()
        tab_nest.children = [data_button_grid, s3_grid]
        tab_nest.set_title(0, 'Local System')
        tab_nest.set_title(1, 'S3')

        grid_dropdowns = widgets.GridspecLayout(22, 12, height='250px')
        grid_dropdowns[0:18, 0:12] = tab_nest
        grid_dropdowns[19:20, 9:11] = btn_data_summary
        grid_dropdowns[19:20, 0:9] = path_output

        def fcn_download_summary(b):
            global df_data
            global path_output

            if df_data.empty is True:
                with path_output:
                    path_output.clear_output()
                    display(print2("Data has not been uploaded yet!"))
            else:
                display(Javascript("IPython.notebook.scroll_to_cell(IPython.notebook.get_selected_index()+1)"))

                display(Javascript(
                    'IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, '
                    'IPython.notebook.get_selected_index()+2)'))

        btn_data_summary.on_click(fcn_download_summary)

        input_accordion = widgets.Accordion(children=[grid_dropdowns])
        input_accordion.set_title(0, 'Data Upload')

        display(input_accordion, s3_output)
    except Exception as e:
        display(print2('Some error occurred. Please check log files for more information'))
        logger.error('Error in fcnUploadAccordionTab. Error: ' + str(e))


def info():
    global df_data

    info_widget = widgets.Output()
    with info_widget:
        if df_data.empty is False:
            info_widget.clear_output()
            df_data.info()

    return info_widget


def fcnReadS3File(bucket_name, file_s3_location, file_name, n_rows=None, header_=True, region_name="us-east-2"):
    '''
    Description:
        Function to read a flat file(csv, xlsx or xlsm) present on S3 into a pandas dataframe

    Arguments:
        bucket_name      : s3 bucket name
        file_s3_location : s3 folder location where files are present in the bucket
        file_name        : Name of the file to be read from s3 location
        n_rows           : This column will be used to read n rows from top of the file while reading it; default value
                            is 'None'
        header_          : This column will be used to set the header property of read_excel or read_csv;  default value
                            is 'True'
        region_name      : Region name of s3 location; default value is 'us-east-2'

    Returns:
        It returns a pandas dataframe of the flat file

    '''

    global access_key
    global secret_key

    # Initializing a boto3 session for establishing a  connection to S3
    session = boto3.session.Session(region_name=region_name)
    s3client = session.client('s3', aws_access_key_id=access_key.value, aws_secret_access_key=secret_key.value)
    key_client = file_s3_location + file_name
    response = s3client.get_object(Bucket=bucket_name, Key=key_client)

    data = None

    if "xlsx" in file_name or "xlsm" in file_name:
        if n_rows is None:
            data = pd.read_excel(io.BytesIO(response['Body'].read()))
        else:
            data = pd.read_excel(io.BytesIO(response['Body'].read()), nrows=n_rows, header=header_)
    elif "csv" in file_name:
        data = pd.read_csv(io.BytesIO(response['Body'].read()), encoding='utf8')

    return data


def fcnLoadUserInputs():
    """
    This function is responsible for the following tasks:
     * reading the input file and fetching columns out of it.
     * showing all the standardization techniques to the user, along with relevant parameters
     * once the input is set by the user, it generates result from it and shows tot he user

    :return: ui made from ipywidget
    """

    global upload
    global data_standardizer
    global scaled_data
    global analysis_df
    global res
    global df_data
    global s3_inp
    global show_result
    global error_widget

    try:
        def fcnMultiSelect():
            global df_data
            global s3_inp

            if not s3_inp:
                col_names = []
                df_data = pd.DataFrame()
                try:
                    if upload.data:
                        try:
                            s = str(upload.data[0], 'utf-8')
                            data_ = io.StringIO(s)
                            df_data = pd.read_csv(data_)
                            if not df_data.empty:
                                col_names = df_data.columns.values.tolist()
                        except Exception as e:
                            print('Unable to read file.')
                            logger.error('Error in fcnMultiSelect, Error: ' + str(e))
                except Exception as e:
                    print('No file uploaded.')
                    logger.error('Error in fcnMultiSelect, Error: ' + str(e))

                return col_names, df_data
            else:
                if not df_data.empty:
                    col_names = df_data.columns.values.tolist()
                    return col_names, df_data

        cols, data = fcnMultiSelect()

        columns_multiselect = widgets.SelectMultiple(
            options=cols,
            description='Fields for analysis:',
            disabled=False,
            style={'description_width': '220px'},
            layout={'width': '440px'},
        )

        correlation_dropdowns = widgets.Dropdown(
            options=types_,
            description='Standardization Type:',
            disabled=False,
            style={'description_width': '150px'}
        )

        min_value = widgets.Text(
            value='0',
            placeholder='Enter min value',
            description='Min value:',
            disabled=False,
            layout={'width': 'max-content'},
            style={'description_width': '120px'},
        )
        max_value = widgets.Text(
            value='1',
            placeholder='Enter min value',
            description='Max value:',
            disabled=False,
            layout={'width': 'max-content'},
            style={'description_width': '120px'},
        )

        quantile_range = widgets.FloatRangeSlider(
            value=[50, 75],
            min=0,
            max=100.0,
            step=0.1,
            description='Quantile Range',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )

        distribution_dropdown = widgets.Dropdown(
            options=['Uniform', 'Normal'],
            description='Distribution :',
            disabled=False,
            style={'description_width': '150px'}
        )

        btn_generate_results = widgets.Button(
            description='Generate Results',
            disabled=False,
            button_style='',
            tooltip='Click to analyse',
            icon='check',
            layout={'width': '240px'}
        )

        btn_compareResults = widgets.Button(
            description='Compare Standardizers',
            disabled=False,
            button_style='',
            tooltip='Click to analyse',
            icon='flask',
            layout={'width': '240px'}
        )

        btn_generate_results.style.button_color = UiConf.inactive_button_color
        btn_compareResults.style.button_color = UiConf.inactive_button_color

        parameter_vbox = widgets.VBox(children=[min_value, max_value])

        def fcnOnValueChange(b):
            if correlation_dropdowns.value == 'Min Max Scaler':
                min_value.value, min_value.description, min_value.placeholder = '0', 'Min value:', 'Enter min value'
                max_value.value, max_value.description, max_value.placeholder = '1', 'Max value:', 'Enter max value'
                parameter_vbox.children = [min_value, max_value]
            elif correlation_dropdowns.value == 'Robust Scaler':
                parameter_vbox.children = [quantile_range]
            elif correlation_dropdowns.value == 'Quantile Scaler':
                parameter_vbox.children = [distribution_dropdown]
            else:
                parameter_vbox.children = []

        correlation_dropdowns.observe(fcnOnValueChange, names='value')

        def fcnGenerateResult(b):

            global data_standardizer
            global scaled_data
            global analysis_df
            global res
            global show_result

            res = True

            try:
                cols, data = fcnMultiSelect()
                cols = list(columns_multiselect.value)
                if cols:

                    data_standardizer = ClsDataStandardizer(data, list(columns_multiselect.value), round_val=2)

                    if correlation_dropdowns.value == 'Min Max Scaler':
                        scaled_data = data_standardizer.apply_min_max_scaler(
                            int(min_value.value), int(max_value.value)).add_column_to_data()

                    elif correlation_dropdowns.value == 'Standard Scaler':
                        scaled_data = data_standardizer.apply_standard_scaler().add_column_to_data()

                    elif correlation_dropdowns.value == 'Min Max Abs Scaler':
                        scaled_data = data_standardizer.apply_max_abs_scaler().add_column_to_data()

                    elif correlation_dropdowns.value == 'Robust Scaler':
                        scaled_data = data_standardizer.apply_robust_scalar(
                            tuple(quantile_range.value)).add_column_to_data()

                    elif correlation_dropdowns.value == 'Quantile Scaler':
                        scaled_data = data_standardizer.apply_quantile_scalar(
                            distribution_dropdown.value.lower()).add_column_to_data()

                    else:
                        scaled_data = data_standardizer.apply_power_scaler().add_column_to_data()

                    analysis_df = scaled_data[scaled_data._get_numeric_data().columns].describe()
                    show_result = True

                    display(Javascript("IPython.notebook.scroll_to_cell(IPython.notebook.get_selected_index()+1)"))
                    display(Javascript(
                        'IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, '
                        'IPython.notebook.ncells())'))
                else:
                    with error_widget:
                        error_widget.clear_output()
                        display(print2("Please select columns"))

            except Exception as e:
                display(print2("Some error occurred. Check log files for more information"))
                logger.error('Error in the function fcnGenerateResult, Error: ' + str(e))

        btn_generate_results.on_click(fcnGenerateResult)

        def fcnCompareResult(b):
            global data_standardizer
            global res
            global show_result

            res = False
            show_result = True

            cols, data = fcnMultiSelect()
            cols = list(columns_multiselect.value)
            try:
                if cols:
                    data_standardizer = ClsDataStandardizer(data, cols, round_val=2)

                    display(Javascript("IPython.notebook.scroll_to_cell(IPython.notebook.get_selected_index()+1)"))

                    display(Javascript(
                        'IPython.notebook.execute_cell_range(IPython.notebook.get_selected_index()+1, '
                        'IPython.notebook.ncells())'))
                else:
                    with error_widget:
                        error_widget.clear_output()
                        display(print2("Please select columns"))

            except Exception as e:
                display(print2("Some error occurred. Check log files for more information"))
                logger.error('Error in the function fcnGenerateResult, Error: ' + str(e))

        btn_compareResults.on_click(fcnCompareResult)

        grid_dropdowns = widgets.GridspecLayout(12, 12, height='180px')

        grid_dropdowns[0:6, :4] = columns_multiselect
        grid_dropdowns[0:3, 5:8] = correlation_dropdowns
        grid_dropdowns[4:, 5:9] = parameter_vbox
        grid_dropdowns[11:, 9:11] = btn_generate_results
        grid_dropdowns[11:, 0:3] = btn_compareResults

        tab = widgets.Accordion(children=[grid_dropdowns])
        tab.set_title(0, 'Select Inputs')

        return display(tab, error_widget)
    except Exception as e:
        display(print2("Some error occurred. Check log files for more information"))
        logger.error('Error in the function fcnLoadUserInputs, Error: ' + str(e))


def fcnResultsTabNew(standardizer_obj, scaled_, analysis_):
    """
    This function is responsible for showing the result of the analysis in the
    dataframe.

    :param standardizer_obj: object from the standardizer class
    :param scaled_: transformed data from the widget
    :param analysis_: contains analysis of the dataframe
    :return: ui widget from the ipywidget
    """
    try:
        scaled_columns = standardizer_obj.make_column_pair()[0]
        # plt.figure(figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
        fcnscatterplot(scaled_, scaled_columns, title='Comparison b/w Normal and Standardize scale',
                       xlabel='index', ylabel=scaled_columns[0], index=True)

        widgets1 = widgets.Output()
        widgets1.layout.width = 'cal(100%)'
        with widgets1:
            display(scaled_.head(10))

        widgets2 = widgets.Output()
        widgets2.layout.width = 'cal(100%)'
        with widgets2:
            analysis_ = analysis_.round(3)
            display(analysis_)

        widgets3 = widgets.Output()
        with widgets3:
            plt.show()

        column_dropdown = widgets.Dropdown(
            options=standardizer_obj.num_cols,
            description='Analyse column:',
            disabled=False,
            style={'description_width': '150px'}
        )

        def fcnOnValueChange(b):
            fcnscatterplot(scaled_,
                           [column_dropdown.value, standardizer_obj.get_column_pair(column_dropdown.value)],
                           title='Comparison b/w Normal and Standardize scale',
                           xlabel='index', ylabel=column_dropdown.value, index=True)

            widgets3.clear_output()
            with widgets3:
                plt.show()

        column_dropdown.observe(fcnOnValueChange, names='value')

        def fcnCreateDownloadLink(df, title="Download Standardized data", filename="scaled_data.csv"):
            csv = df.to_csv()
            b64 = base64.b64encode(csv.encode())
            payload = b64.decode()
            html = '<button class="p-Widget jupyter-widgets jupyter-button widget-button" ' \
                   'style="width: 240px; ' \
                   'background-color: orange;"><i class="fa fa-download"></i>' \
                   '<a download="{filename}" href="data:text/csv;base64,{payload}" ' \
                   'target="_blank" style="color:white">{title}</a></button>'
            html = html.format(payload=payload, title=title, filename=filename)
            return html

        scaled_data_grid = widgets.GridspecLayout(12, 12)
        scaled_data_grid[0:1, 9:11] = widgets.HTML(value=fcnCreateDownloadLink(scaled_))
        scaled_data_grid[2:, :] = widgets1

        analysis_data_grid = widgets.GridspecLayout(12, 12)
        analysis_data_grid[0:1, 9:11] = widgets.HTML(
            value=fcnCreateDownloadLink(analysis_, title="Download Analysis", filename='analysis.csv'))
        analysis_data_grid[2:, :] = widgets2

        chart_data_grid = widgets.GridspecLayout(12, 3)
        chart_data_grid[0:1, 0:1] = column_dropdown
        chart_data_grid[:, 1:] = widgets3

        tab_nest = widgets.Tab()
        tab_nest.children = [scaled_data_grid, analysis_data_grid, chart_data_grid]
        tab_nest.set_title(0, 'Standardized data')
        tab_nest.set_title(1, 'Analysis')
        tab_nest.set_title(2, 'Field Comparison')

        grid_dropdowns = widgets.GridspecLayout(12, 12, height='550px')

        grid_dropdowns[0:12, 0:12] = tab_nest
        input_accordion = widgets.Accordion(children=[grid_dropdowns])
        input_accordion.set_title(0, 'Results')

        return display(input_accordion)
    except Exception as e:
        display(print2("Some error occurred. Check log files for more information"))
        logger.error('Error in the function fcnLoadUserInputs, Error: ' + str(e))


def fcnComparisionTabNew(standardizer_obj):
    """
    This function shows the comparision of the different standardizers.
    :param standardizer_obj: obj of the clas standardizer widget.
    :return: ui from the ipywidget
    """

    try:
        num_cols = standardizer_obj.num_cols

        all_scaled_data = data_standardizer.apply_all_scaler()

        def fcnMatchingColumns(column):
            temp = []
            for each_column in all_scaled_data.columns:
                if column in each_column:
                    temp.append(each_column)
            return temp

        matching_cols = fcnMatchingColumns(num_cols[0])
        min_max_scaled_data = all_scaled_data[matching_cols].to_numpy()
        plt.figure(figsize=(9, 6), dpi=85, facecolor='w', edgecolor='k')
        plt.title('Comparison b/w Normal and Standardize scale')
        plt.boxplot(min_max_scaled_data, showfliers=False)
        plt.xticks(range(1, len(matching_cols) + 1), matching_cols, rotation='vertical')
        plt.ylabel(num_cols[0])
        widgets3 = widgets.Output()
        with widgets3:
            plt.show()

        column_dropdown = widgets.Dropdown(
            options=standardizer_obj.num_cols,
            description='Analyse column:',
            disabled=False,
            style={'description_width': '150px'}
        )

        def fcnOnValueChange(b):
            matching_cols = fcnMatchingColumns(column_dropdown.value)
            min_max_scaled_data = all_scaled_data[matching_cols].to_numpy()
            plt.figure(figsize=(9, 6), dpi=85, facecolor='w', edgecolor='k')
            plt.title('Comparison b/w Normal and Standardize scale')
            plt.boxplot(min_max_scaled_data, showfliers=False)
            plt.xticks(range(1, len(matching_cols) + 1), matching_cols, rotation='vertical')
            plt.ylabel(column_dropdown.value)
            widgets3.clear_output()
            with widgets3:
                plt.show()

        column_dropdown.observe(fcnOnValueChange, names='value')

        grid_dropdowns_res = widgets.GridspecLayout(500, 12)

        box_layout = widgets.Layout(display='inline-flex',
                                    flex_flow='column',
                                    justify_content='space-between',
                                    justify_items='center',
                                    align_items='center',
                                    )

        box = widgets.HBox(children=[column_dropdown, widgets3], layout=box_layout)
        grid_dropdowns_res[:, :] = box
        tab_res = widgets.Accordion()
        tab_res.set_title(0, 'Comparision b/w different Scalers')

        tab_res.children = [grid_dropdowns_res]
        return tab_res
    except Exception as e:
        display(print2('Some error occurred. Please check log files for more information'))
        logger.error('Error in comparision tab                        . Error: ' + str(e))


def fcnscatterplot(frame, columns, xlabel, ylabel, title, index=False):
    '''
    :param frame: dataframe which needs to be ploted
    :param columns: columns as the axis
    :param xlabel: labels for the columns
    :param ylabel: labels for the columns
    :param title: title for the graph
    :param index:
    :return: a scatter plot
    '''
    try:
        plt.figure(figsize=(16, 6), dpi=82, facecolor='w', edgecolor='k')
        plt.subplot(131)
        plt.plot(range(frame.shape[0]), frame[columns[0]], color='blue', alpha=0.5, label=columns[0])
        plt.title(title)
        plt.legend(loc='upper left')
        plt.ylabel(ylabel)
        plt.grid()
        plt.subplot(132)
        plt.plot(range(frame.shape[0]), frame[columns[1]], color='green', alpha=0.5, label=columns[1])
        # plt.suptitle(title)
        plt.legend(loc='upper left')
        plt.grid()
    except Exception as e:
        display(print2("Error in making the graph, Function name: fcnscatterPlot"))
        logger.error('"Error in making the graph, Function name: fcnscatterPlot, Error: ' + str(e))


def fcnResultCompare():
    '''
    This method is used to divert the code flow from generate result and compare standardizer
    :return:
    '''

    global data_standardizer
    global scaled_data
    global analysis_df
    global res
    global show_result
    global error_widget

    clear_output()
    error_widget.clear_output()

    if show_result:
        if res:
            return fcnResultsTabNew(data_standardizer, scaled_data, analysis_df)
        else:
            return fcnComparisionTabNew(data_standardizer)
    else:
        display(print3('Waiting for inputs...'))
