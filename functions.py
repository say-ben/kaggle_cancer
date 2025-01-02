import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def aggregate_table(data, factor, columns, aggs):

    tab = pd.DataFrame()

    for i, col in enumerate(columns):
        if aggs[i] == 'count':
            tab_new = data[[factor, columns[i]]].groupby(factor, observed=True).count()
        if aggs[i] == 'mean':
            tab_new = data[[factor, columns[i]]].groupby(factor, observed=True).mean()
        if aggs[i] == 'sum':
            tab_new = data[[factor, columns[i]]].groupby(factor, observed=True).sum()

        tab = pd.concat([tab, tab_new], axis=1)
    
    tab = tab.reset_index()

    return tab



def plotly_plot(x, y_list, y_names=[None]*10, secondary_y=[False]*10, plot_type=['scatter']*10, colours=None, title=None, x_title=None, y_title=None, y2_title=None, dims=[900,600], x_range=None, y_range=None, y2_range=None):
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    for i, y in enumerate(y_list):
        if plot_type[i] == "bar":
            fig.add_trace(go.Bar(name=y_names[i], x=x, y=y, marker=dict(color=colours[i])), secondary_y=secondary_y[i])
        if plot_type[i] == "scatter":
            fig.add_trace(go.Scatter(name=y_names[i], x=x, y=y, marker=dict(color=colours[i])), secondary_y=secondary_y[i])

    fig.update_layout(title_text=title, width=dims[0], height=dims[1])
    fig.update_xaxes(title_text=x_title, range=x_range)
    fig.update_yaxes(title_text=y_title, secondary_y=False, range=y_range)

    if y2_title != None:
        fig.update_yaxes(title_text=y2_title, secondary_y=True, range=y2_range)
        fig['layout']['yaxis2']['showgrid'] = False

    return fig