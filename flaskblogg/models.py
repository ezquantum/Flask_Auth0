import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskblogg import app
from flask_login import UserMixin

###################
# database_name = "blogatog"
project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
db = SQLAlchemy(app)

#dev variable not hidden
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://epixojdhlwjsir:99617ba473d3f6609a9c93439e87bb31fb1ac9fa6d5d167e66e2e29d703261f0@ec2-52-71-153-228.compute-1.amazonaws.com:5432/d93kgv3fnkj0fg'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


###################
def Guest():
    #create a dict for guest user
    return dict({'id':-1,
        'username':'Guest',
        'email':'',
        'posts':None})

    

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    image_file = db.Column(db.String(200), nullable=True,
                           default='default.jpg')
    password = db.Column(db.String(120), unique=False, nullable=True)
    last_login_date = db.Column(db.DateTime, nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f"Author('{self.username}', '{self.email}', '{self.image_file}', '{self.id}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=True,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
 
db_drop_and_create_all()
