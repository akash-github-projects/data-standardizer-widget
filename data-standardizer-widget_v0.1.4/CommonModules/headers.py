"""
This is a generic function for displaying headers across all widgets.

"""

import warnings
import ipywidgets as widgets
from IPython.display import display, HTML, Image, Javascript
import os

warnings.filterwarnings('ignore')


def fcn_display_headers(imgname="analytechs_widget.jpg"):
    output = widgets.Output()
    with output:
        js = '''
               function code_toggle() {
                if (document.getElementById('switch-orange').checked){
                $('div.input').show();
                } else {
                $('div.input').hide();
                }
                code_show = !code_show
               } 
               $( document ).ready(code_toggle);
               setInterval(code_toggle,1000);

               '''
        js = Javascript(js)
        display(js)

        display(HTML('''<meta charset="utf-8">
        <link rel="stylesheet" href="Resources/SupportFiles/css/generic_design.css">

        <form class='toggles' action="javascript:IPython.notebook.execute_cells_below()">
                <button type="submit" id="toggleButton" style="position:relative; float:right; border:none; background-color:white; padding-top:5px; padding-right:30px;">
                    <img src = "Resources/SupportFiles/images/refresh_icon.png" />
                   <span class="tooltiptext">Reset</span>
                </button>
                <div class="code-toggle">
                    <label>Code toggle</label>
                </div>
                <div class="button-switch code-toggle">
                  <input type="checkbox" id="switch-orange" class="switch" />
                  <label for="switch-orange" class="lbl-off">Off</label>
                  <label for="switch-orange" class="lbl-on">On</label>
                </div>
            </div>
        </form>



    '''))

        display(HTML('''
            <style>
                .jupyter-widgets.widget-tab > .p-TabBar .p-TabBar-tab {
                    flex: 0 1 250px
                }
            </style>

        '''))

        display(HTML("<style>.container { width:98% !important; }</style>"))

        display(Image(filename="Resources" + os.sep + "SupportFiles" + os.sep + "images" + os.sep + imgname,
                      width="1500px", height="230px"))

        display(HTML('<style>.prompt{width: 0px; min-width: 0px; visibility: collapse}</style>'))

        display(widgets.HTML(
            value="<i><font color={}>This tool is solely for the use of ZS personnel. No part of it may be circulated, quoted or reproduced for distribution outside without prior written approval of ZS Associates</i>".format(
                'gray')))

        display(Javascript("""IPython.keyboard_manager.disable()"""))
    return output
