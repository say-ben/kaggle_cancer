import pandas as pd
import numpy as np
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



def numerical_summary(df, cols):

    tab = pd.DataFrame(columns = ['Total Rows', 'Missing Rows', 'Populated Rows', 'Unique Values', 'Maximum', 'Minimum', 'Range', 
                                  'Median', 'Upper Quartile', 'Lower Quartile', 'IQR', 'Variance', 'Std Deviation'])

    for i in cols:
        total_rows = len(df)
        missing_rows = df[i].isna().sum()
        populated_rows = total_rows - missing_rows
        unique_values = len(df[i].unique())
        maximum = df[i].max()
        minimum = df[i].min()
        range = maximum - minimum
        median = df[i].median()
        upper_quartile = np.percentile(df[i], 75)
        lower_quartile = np.percentile(df[i], 25)
        iqr = upper_quartile - lower_quartile
        var = df[i].var()
        stdev = df[i].std()

        tab.loc[i] = [total_rows, missing_rows, populated_rows, unique_values, maximum, minimum, range, median, upper_quartile, lower_quartile, iqr, var, stdev]
    
    return tab



def categorical_summary(df, cols):

    tab = pd.DataFrame(columns = ['Feature', 'Type', 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', 'Level 6', 'Level 7', 'Level 8', 'Level 9', 'Level 10', 'Missing'])
    
    for e, i in enumerate(cols):

        value_counts = df[i].value_counts()
        levels = list(value_counts.index)
        values = list(value_counts)
        other = pd.Series(values[10:]).sum()
        missing = df[i].isna().sum()
        if other > 0:
            levels = levels[:9] + ['Other']
            values = values[:9] + [other]
        levels = levels + ['-'] * 10
        values = values + ['-'] * 10
        levels = levels[:10] + ['Missing']
        values = values[:10] + [missing]
        tab.loc[2*e] = [i, 'Levels'] + levels[:11]
        tab.loc[2*e+1] = [i, 'Counts'] + values[:11]

    return tab