'''
This file is for applying CSS to the UI properties of the widget.

'''

import warnings
from IPython.display import display, HTML
warnings.filterwarnings('ignore')


def fcn_load_resources():
    
    '''
    Purpose : To applys CSS properties for all HTML elements
    Parameters : None
    
    '''
    
    display(HTML('''<meta charset="utf-8">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            <link rel="stylesheet" type="text/css" href="Resources/SupportFiles/css/generic_design.css">'''))

