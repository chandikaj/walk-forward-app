import os
import secrets
from flask import Flask 

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

para_file_name = 'parameters_' + secrets.token_hex(6) + '.txt'
graph_file_name = 'optimal_graph_' + secrets.token_hex(6) + '.json'

# Global Variables
fitness_function = 1
daily_returns = None 
pvals = None
X_test_default = 0 
dest = os.path.join(app.root_path, 'static')
    
from walkforward import routes