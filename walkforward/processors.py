import pandas as pd
import numpy as np
import itertools as it

def process_input_file(daily_returns, fitness_function):
    drop_cols = list(it.chain(range(0, len(daily_returns.columns), 5), range(fitness_function, len(daily_returns.columns), 5)))
    drop_cols.sort()
    daily_returns = daily_returns.loc[:, drop_cols]

    def el_to_dt(cell):
        yr = int(cell/10000) + 1900
        mth = cell-int(cell/10000)*10000
        mth = int(mth/100)
        day = cell - int(cell/100)*100
        return pd.datetime(yr, mth, day).date()

    dates_as_cols = {}
    for cn in daily_returns.columns:
        if (cn-fitness_function) % 5 == 0:
            dates_as_cols[cn] = el_to_dt(daily_returns.loc[0, cn-fitness_function])
            drop_cols.append(cn-fitness_function)

    daily_returns = daily_returns.rename(columns=dates_as_cols).loc[:, dates_as_cols.values()]

    daily_returns.index.name = 'perm_id'

    daily_returns = daily_returns.T

    daily_returns -= daily_returns.shift(1)
    daily_returns.fillna(0, inplace=True)
    daily_returns.index = pd.to_datetime(daily_returns.index)

    daily_returns_dates = daily_returns.reset_index()
    daily_returns_dates = daily_returns_dates[['index']]
    daily_returns_wf = daily_returns.reset_index(drop = True)
    
    return daily_returns_dates, daily_returns_wf

   