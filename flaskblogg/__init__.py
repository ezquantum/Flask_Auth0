import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# this app is imported
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
database_name = "blogatog"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://Amajimoda@localhost:5432/blogatog' #local
# db = SQLAlchemy(app)

from flaskblogg import routes

