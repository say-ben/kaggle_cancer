import pandas as pd

def aggregate_table(data, factor, columns, aggs):

    tab = pd.DataFrame()

    for i, col in enumerate(columns):
        if aggs[i] == 'count':
            tab_new = data[[factor, columns[i]]].groupby(factor).count()
        if aggs[i] == 'mean':
            tab_new = data[[factor, columns[i]]].groupby(factor).mean()
        if aggs[i] == 'sum':
            tab_new = data[[factor, columns[i]]].groupby(factor).sum()

        tab = pd.concat([tab, tab_new], axis=1)

    return tab



