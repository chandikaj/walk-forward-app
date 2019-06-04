from walkforward.processors import process_input_file
from walkforward.wf_functions import anchored, un_anchored
from walkforward.default_plot import run_default, create_default
from walkforward.default_ts import out_put_ts
from walkforward.fitness_plot import run_fitness
from walkforward.fitness_ts import out_put_fs


def master_func_tradesT(in_period, out_period, daily_returns, pvals, dest, un_anchored_check):
    daily_returns_dates, daily_returns_wf = process_input_file(
        daily_returns, 1)

    if un_anchored_check == True:
        X_train, X_test, un_anchored_check = un_anchored(
            in_period, out_period, daily_returns_wf)
        opt = run_default(X_train, X_test)
        out_put_ts(X_train, X_test, opt, daily_returns_dates, daily_returns_wf,
                   in_period, out_period, pvals, dest, un_anchored_check=True)
    else:
        X_train, X_test = anchored(in_period, out_period, daily_returns_wf)
        opt = run_default(X_train, X_test)
        out_put_ts(X_train, X_test, opt, daily_returns_dates, daily_returns_wf,
                   in_period, out_period, pvals, dest, un_anchored_check=False)


def master_func_tradesF(in_period, out_period, fitness_function, daily_returns, pvals, un_anchored_check):
    X_train_default, X_test_default = create_default(in_period, out_period, daily_returns, un_anchored_check)
    daily_returns_dates, daily_returns_wf = process_input_file(
        daily_returns, fitness_function)

    if un_anchored_check == True:
        X_train, X_test, un_anchored_check = un_anchored(
            in_period, out_period, daily_returns_wf)
        opt = run_fitness(X_train, X_test_default)
        out_put_fs(X_train, X_test, opt, daily_returns_dates, daily_returns_wf,
                   in_period, out_period, pvals, fitness_function, un_anchored_check=True)
    else:
        X_train, X_test = anchored(in_period, out_period, daily_returns_wf)
        opt = run_fitness(X_train, X_test_default)
        out_put_fs(X_train, X_test, opt, daily_returns_dates, daily_returns_wf,
                   in_period, out_period, pvals, fitness_function, un_anchored_check=False)
