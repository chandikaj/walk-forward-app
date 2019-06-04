def anchored(in_period, out_period, daily_returns_wf):
    X_train = []
    X_test = []
    n_records = len(daily_returns_wf)
    for i in range(in_period, n_records, out_period):
        X_train.append(daily_returns_wf[0:i])
        X_test.append(daily_returns_wf[i:i+(out_period)])

    return X_train, X_test

def un_anchored(in_period, out_period, daily_returns_wf):
    un_anchored_check = True
    X_train = []
    X_test = []
    var = in_period + out_period
    n_records = len(daily_returns_wf)
    for i in range(var, n_records, out_period):
        X_train.append(daily_returns_wf[i-(var):i-(out_period)])
        X_test.append(daily_returns_wf[i-(out_period):i])

    return X_train, X_test, un_anchored_check

def last_batch(X_train, X_test, daily_returns_wf, in_period, out_period):
    last_batch_in_period_start = X_train[-1].index[(int(out_period))]
    last_batch_in_period_end = last_batch_in_period_start + in_period
    last_batch_out_period_start = X_test[-1].index[-1] + 1
    last_batch_out_period_end = len(daily_returns_wf)

    last_batch_in_period = daily_returns_wf.iloc[last_batch_in_period_start:last_batch_in_period_end,:]
    last_batch_out_period = daily_returns_wf.iloc[last_batch_out_period_start: last_batch_out_period_end,:]  

    sum_last_batch = last_batch_in_period.sum(axis = 0)
    max_param_last_batch = sum_last_batch.idxmax()
    opt_last_batch = last_batch_out_period[max_param_last_batch]

    return last_batch_in_period, last_batch_out_period, sum_last_batch, max_param_last_batch, opt_last_batch