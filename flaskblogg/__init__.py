from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# this app is imported
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
database_name = "blogatog"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://Amajimoda@localhost:5432/blogatog'
# db = SQLAlchemy(app)

from flaskblogg import routes

