import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from boto.s3.connection import S3Connection
# from flask_login import LoginManager

s3 = S3Connection(os.environ['SECRET_KEY'], os.environ['DATABASE_URL'])
# this app is imported
app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' #yes it's a dummy site... it's fine
database_name = "blogatog"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://epixojdhlwjsir:99617ba473d3f6609a9c93439e87bb31fb1ac9fa6d5d167e66e2e29d703261f0@ec2-52-71-153-228.compute-1.amazonaws.com:5432/d93kgv3fnkj0fg'
# db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# login_manager=LoginManager(app)

from flaskblogg import routes

