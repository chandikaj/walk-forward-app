import os 
import pandas as pd
from walkforward.wf_functions import anchored, un_anchored, last_batch

def out_put_ts(X_train, X_test, opt, daily_returns_dates, daily_returns_wf, in_period, out_period, pvals, dest, un_anchored_check):
    
    if un_anchored_check == True:
        
        last_batch_in_period, last_batch_out_period, sum_last_batch, max_param_last_batch, opt_last_batch = last_batch(X_train, X_test, daily_returns_wf, in_period, out_period)
        
        out_put = []
        for i in opt:
            out_put.append(i.to_frame())

        days = []    
        parameter = []
        start_date = []
        end_date = []
        net_profit = []
        for i in out_put:
            days.append(len(i))
            parameter.append(int(i.columns._data))
            start_date.append(daily_returns_dates.loc[i.index[0]])
            end_date.append(daily_returns_dates.loc[i.index[-1]])
            net_profit.append(int(i.sum().values))

        days = days + [len(last_batch_out_period)]
        parameter = parameter + [max_param_last_batch]
        start_date = start_date + [daily_returns_dates.loc[last_batch_out_period.index[0]]]
        end_date = end_date + [daily_returns_dates.loc[last_batch_out_period.index[-1]]]
        net_profit = net_profit + [opt_last_batch.sum()]   

        out_put_table = (pd.DataFrame([days, parameter, start_date, end_date, net_profit])).T
        out_put_table = out_put_table.rename(columns = {
                0: 'Days',
                1: 'Best parameter',
                2: 'Start Date',
                3: 'End Date',
                4: 'Net Profit',
                }
            )
        out_put_table['Equity Curve'] = out_put_table['Net Profit'].cumsum()
        out_put_table = out_put_table[['Start Date', 'End Date', 'Days', 'Best parameter', 'Net Profit', 'Equity Curve']]
        out_pvals = pvals.loc[out_put_table['Best parameter']].reset_index(drop = True)
        out_put_table = (out_put_table.join(out_pvals, how ='inner'))


        def dt_to_el(cell):
            cell = cell.iloc[0]
            year = (cell.year- 1900)
            month = cell.strftime('%m')
            day = cell.strftime('%d')
            return str(year) + month + day

        path = os.path.join(dest, 'ts_output.txt')

        with open(path, 'w') as output_file:
            for r in range(len(out_put_table)):
                print(f'if date >= {dt_to_el(out_put_table["Start Date"].loc[r])} and date <= {dt_to_el(out_put_table["End Date"].loc[r])}  then // \nbegin', file = output_file)
                for t in range(len(out_pvals.columns)):
                    print(f'  {out_pvals.columns[t]} = {out_pvals.iloc[r,t]};', file = output_file)
                print(f'end;', file = output_file)                

    else:
        out_put = []
        for i in opt:
            out_put.append(i.to_frame())

        days = []    
        parameter = []
        start_date = []
        end_date = []
        net_profit = []
        for i in out_put:
            days.append(len(i))
            parameter.append(int(i.columns._data))
            start_date.append(daily_returns_dates.loc[i.index[0]])
            end_date.append(daily_returns_dates.loc[i.index[-1]])
            net_profit.append(int(i.sum().values))

        days = days
        parameter = parameter
        start_date = start_date 
        end_date = end_date 
        net_profit = net_profit 

        out_put_table = (pd.DataFrame([days, parameter, start_date, end_date, net_profit])).T
        out_put_table = out_put_table.rename(columns = {
                0: 'Days',
                1: 'Best parameter',
                2: 'Start Date',
                3: 'End Date',
                4: 'Net Profit',
                }
        )
        out_put_table['Equity Curve'] = out_put_table['Net Profit'].cumsum()
        out_put_table = out_put_table[['Start Date', 'End Date', 'Days', 'Best parameter', 'Net Profit', 'Equity Curve']]
        out_pvals = pvals.loc[out_put_table['Best parameter']].reset_index(drop = True)
        out_put_table = out_put_table.join(out_pvals, how ='inner')

        def dt_to_el(cell):
            cell = cell.iloc[0]
            year = (cell.year- 1900)
            month = cell.strftime('%m')
            day = cell.strftime('%d')
            return str(year) + month + day

        path = os.path.join(dest, 'ts_output.txt')
        
        with open(path, 'w') as output_file:
            for r in range(len(out_put_table)):
                print(f'if date >= {dt_to_el(out_put_table["Start Date"].loc[r])} and date <= {dt_to_el(out_put_table["End Date"].loc[r])}  then // \nbegin', file = output_file)
                for t in range(len(out_pvals.columns)):
                    print(f'  {out_pvals.columns[t]} = {out_pvals.iloc[r,t]};', file = output_file)
                print(f'end;', file = output_file)                