import ipywidgets as widgets


def print2(text):
    wid = widgets.HTML(value=f"<b><font color='red'>{text}</b>")
    return wid


def print3(text):
    wid = widgets.HTML(value=f"<b><font color='green'>{text}</b>")
    return wid


def print4(text):
    wid = widgets.HTML(value=f"<b><font color='#2B3BC5'>{text}</b>")
    return wid
