import os
import secrets
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Setting up Flask-Session object
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Global Variables
fitness_function = 1
daily_returns = None
pvals = None
X_test_default = 0
dest = os.path.join(app.root_path, 'static')

from walkforward import routes