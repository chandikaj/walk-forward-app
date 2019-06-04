import pandas as pd
from walkforward.processors import process_input_file
from walkforward.wf_functions import anchored, un_anchored

def run_default(X_train, X_test):
    opt = []
    for i, p in zip(X_train, X_test):
        opt.append(p[i.sum(axis = 0).idxmax()])

    return opt

def create_equity_default(X_train, X_test):
    performance = pd.DataFrame(pd.concat(run_default(X_train, X_test), axis = 0, join = 'inner'))
    performance = performance.rename(columns = { 0 : 'MtM_Pl'})
    performance['equity'] = performance['MtM_Pl'].cumsum()
    return performance['equity']

def create_default(in_period, out_period, daily_returns, un_anchored_check):
    daily_returns_dates, daily_returns_wf = process_input_file(daily_returns, 1)
    
    if un_anchored_check == True:
        X_train, X_test, un_anchored_check = un_anchored(in_period, out_period, daily_returns_wf)
    else:
        X_train, X_test = anchored(in_period, out_period, daily_returns_wf)
    
    return X_train, X_test