import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

# this app is imported
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #yes it's a dummy site... it's fine
database_name = "blogatog"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager=LoginManager(app)

from flaskblogg import routes

