import os
import json 
import pandas as pd
from flask import render_template, redirect, url_for, request, send_file
from walkforward import app, para_file_name, graph_file_name, daily_returns, pvals, X_test_default, dest 
from walkforward.forms import UploadFileForm
from walkforward.create_plotly_graphs import make_plotly_plots
from walkforward.ts_masters import master_func_tradesF, master_func_tradesT


@app.route("/", methods=['GET', 'POST'])
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = UploadFileForm()
    message = ""
    category = False
    multichart = None
    singlechart = None
    global daily_returns
    global pvals

    if form.validate_on_submit:
        if form.data_files.data:
            for files in form.data_files.data:
                if "Parameter" not in files.filename:
                    daily_returns = pd.read_csv(files, header=None)
                if "ParameterValues" in files.filename:
                    pvals = pd.read_csv(files, header=None)
                if "ParameterNames" in files.filename:
                    pnames = pd.read_csv(files, header=None)

            pvals.rename(columns={x: pnames.loc[0, x]
                                  for x in pnames.columns}, inplace=True)
            pvals.index.name = 'perm_id'
            pnames = None

            message = "Files were uploaded successfully"
            category = True

    return render_template('upload.html', form=form, message=message,
                           category=category)


@app.route("/graphs", methods=['POST', 'GET'])
def graphs():

    if daily_returns is None:
        return redirect(url_for('upload'))
    else:
        wf_type = request.form.get('type_select')
        un_anchored_check = False

        if wf_type == 'Unanchored':
            un_anchored_check = True

        in_period = request.form.get('in_sample')
        out_period = request.form.get('out_sample')
        in_period = 500 if in_period is '' else int(in_period)
        out_period = 120 if out_period is '' else int(out_period)

        # Select widget option generation 
        path = os.path.join(dest, graph_file_name)
        option_list = []

        if request.form.get('Download_output') == 'Download_output':

            selected_optimal = request.form.get('ts_output_select') 
            in_period = int(selected_optimal.split('_')[2].split('-')[1])
            out_period = int(selected_optimal.split('_')[3].split('-')[1])
            fitness_function = int(selected_optimal.split('_')[0][1])
            anchor_type = selected_optimal.split('_')[1]

            if anchor_type == 'Unanchored':
                un_anchored_check = True
            else:
                un_anchored_check = False

            if fitness_function == 1:
                master_func_tradesT(in_period, out_period, daily_returns, pvals, dest, un_anchored_check)
            else:
                master_func_tradesF(in_period, out_period, fitness_function, daily_returns, pvals, un_anchored_check)

            filename = selected_optimal + '.txt'
            path_output =  os.path.join(dest, 'ts_output.txt')
            return send_file(path_output, mimetype='text', attachment_filename=filename, as_attachment=True, cache_timeout=0)

        if request.form.get('Create_Graph') == 'Create_Graph':

            parameters = [in_period, out_period, un_anchored_check]

            # Writing the parameters to a file
            with open(os.path.join(dest, para_file_name), 'w') as f:
                for item in parameters:
                    f.write(str(item) + '\n')

            multichart, single_charts = make_plotly_plots(in_period, out_period, daily_returns, un_anchored_check, 
                                                                                            optimal=None, create_best=False)

            if os.path.isfile(path) == True:
                with open(path, 'r') as infile:
                    figure = json.load(infile)

                for item in figure['data']:
                    option_list.append(item['name'])
            
            return render_template('graphs_one.html', plot_1=multichart, plot_2=single_charts[0], plot_3=single_charts[1], 
                                    plot_4=single_charts[2], plot_5=single_charts[3], option_list=option_list)

        elif request.form.get('Update_best') == 'Update_best':

            with open(os.path.join(dest, para_file_name), 'r') as f:
                para = f.readlines()

            in_period, out_period, un_anchored_check = [w.strip('\n') for w in para]
          
            optimal_function = request.form.get('optimal')
            best_lines = make_plotly_plots(int(in_period), int(out_period), daily_returns, 
                                                                      eval(un_anchored_check), optimal=optimal_function, create_best=True)
            
            if os.path.isfile(path) == True:
                with open(path, 'r') as infile:
                    figure = json.load(infile)

                for item in figure['data']:
                    option_list.append(item['name'])

            return render_template('graphs_second.html', plot_6=best_lines, option_list=option_list)