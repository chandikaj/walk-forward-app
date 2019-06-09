import json
import os
import plotly
from plotly.tools import make_subplots
import plotly.graph_objs as go
from walkforward.default_plot import create_default, create_equity_default
from walkforward.fitness_plot import create_fitness, create_equity_fitness
from walkforward import dest


def make_plotly_plots(in_period, out_period, daily_returns, un_anchored_check, graph_file_name, optimal, create_best):

    if un_anchored_check is True:
        anchor_status = "Unanchored"
    else:
        anchor_status = "Anchored"

    # Default Trace
    X_train_default, X_test_default = create_default(
        in_period, out_period, daily_returns, un_anchored_check)
    y_data = create_equity_default(X_train_default, X_test_default)
    x_data = y_data.index
    trace1 = go.Scatter(x=x_data, y=y_data, mode='lines',
                        name='FF1_{}_In-{}_Out-{}'.format(anchor_status, in_period, out_period))

    # Fitness_1 Trace
    X_train, X_test = create_fitness(
        in_period, out_period, 2, daily_returns, un_anchored_check)
    y_data = create_equity_fitness(X_train, X_test_default, 2)
    x_data = y_data.index
    trace2 = go.Scatter(x=x_data, y=y_data, mode='lines',
                        name='FF2_{}_In-{}_Out-{}'.format(anchor_status, in_period, out_period))

    # Fitness_2 Trace
    X_train, X_test = create_fitness(
        in_period, out_period, 3, daily_returns, un_anchored_check)
    y_data = create_equity_fitness(X_train, X_test_default, 3)
    x_data = y_data.index
    trace3 = go.Scatter(x=x_data, y=y_data, mode='lines',
                        name='FF3_{}_In-{}_Out-{}'.format(anchor_status, in_period, out_period))

    # Fitness_3 Trace
    X_train, X_test = create_fitness(
        in_period, out_period, 4, daily_returns, un_anchored_check)
    y_data = create_equity_fitness(X_train, X_test_default, 4)
    x_data = y_data.index
    trace4 = go.Scatter(x=x_data, y=y_data, mode='lines',
                        name='FF4_{}_In-{}_Out-{}'.format(anchor_status, in_period, out_period))

    # MultiLine chart
    data = [trace1, trace2, trace3, trace4]
    layout = go.Layout(title='Multiline Fitness graph', xaxis=dict(
        range=[0, x_data[-1]]), legend=dict(orientation="h"))
    figure = go.Figure(data, layout)

    path = os.path.join(dest, 'multilineGraph.txt')

    multilineJSON = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)

    # Singleine charts
    layout1 = go.Layout(title='FF1 - NetProfit', xaxis=dict(title='Out Period Trading Days',
                                                            range=[0, x_data[-1]]), yaxis=dict(title='Net Profit'))
    layout2 = go.Layout(title='FF2 - Current Profit Factor', xaxis=dict(
        title='Out Period Trading Days', range=[0, x_data[-1]]), yaxis=dict(title='Net Profit'))
    layout3 = go.Layout(title='FF3 - Return on Account', xaxis=dict(
        title='Out Period Trading Days', range=[0, x_data[-1]]), yaxis=dict(title='Net Profit'))
    layout4 = go.Layout(title='FF4 - Weighted ROA', xaxis=dict(
        title='Out Period Trading Days', range=[0, x_data[-1]]), yaxis=dict(title='Net Profit'))

    fig1 = go.Figure([trace1], layout1)
    fig2 = go.Figure([trace2], layout2)
    fig3 = go.Figure([trace3], layout3)
    fig4 = go.Figure([trace4], layout4)

    singlechart1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    singlechart2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    singlechart3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    singlechart4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)

    single_charts = [singlechart1, singlechart2, singlechart3, singlechart4]

    path = os.path.join(dest, graph_file_name)

    if optimal == 'F1':
        best_func = singlechart1
    elif optimal == 'F2':
        best_func = singlechart2
    elif optimal == 'F3':
        best_func = singlechart3
    else:
        best_func = singlechart4

    if create_best:
        if os.path.isfile(path) == False:
            with open(path, 'w') as outfile:
                outfile.write(best_func)
            figure = json.loads(best_func)
        else:
            with open(path, 'r') as infile:
                figure = json.load(infile)

            new_trace = json.loads(best_func)
            figure['data'].append(new_trace['data'][0])

            with open(path, 'w') as outfile:
                json.dump(figure, outfile)

        figure['layout']['title']['text'] = 'Selected optimal fitness functions'
        figure['layout']['xaxis']['range'] = (0, (x_data[-1]+200))
        figure['layout']['xaxis']['title'] = ""
        figure['layout'].update({'legend': {'orientation': 'h'}})
        best_lines = json.dumps(figure, cls=plotly.utils.PlotlyJSONEncoder)
        return best_lines
    else:
        return multilineJSON, single_charts
