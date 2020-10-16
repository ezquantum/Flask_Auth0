import os
import datetime
from urllib.request import urlopen
from flask import request, _request_ctx_stack, abort, Flask, jsonify, render_template, url_for, flash, session, redirect, g
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from os import environ as env
from flaskblogg import app
import json
from functools import wraps, update_wrapper
from flask_cors import CORS, cross_origin
from flaskblogg.forms import RegistrationForm, LoginForm, PostForm
from jose import jwt
from flaskblogg.models import User, Post, db, db_drop_and_create_all
from .auth import auth
from .auth.auth import AuthError, require_auth_from_session
from flask_login import current_user


# from flaskblog.auth import AuthError, requires_auth

# db.create_all()
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'Login'

# @login_manager.user_loader
# def load_user(user_id):
#     return UserInfo.query.get(int(user_id))

# class LoginManager(app=None, add_context_processor=True)
# def load_user(session):


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

# native registration supported


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password = form.password.data,
            last_login_date = datetime.datetime.now()
        )

        # insert the user
        db.session.add(user)
        db.session.commit() 
 
        session['profile'] = {
            'name': form.username.data,
            'email': form.email.data,
            'permission':'EDITOR'
        }   
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data == 'admin@blog.com' and form.password.data == 'password':
#             flash('You have been logged in!', 'success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#     return render_template('login.html', title='Login', form=form)

@app.route('/login')
def login():
    # # redirect_uri = url_for('authorize', _external=True)

    return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

    ###########test###########
    # import http.client

    # conn = http.client.HTTPSConnection("coffestack.us.auth0.com")

    # payload = "{\"client_id\":\"KoJK3ZANDBUo3MqQ89kuJDihHyorWMHG\",\"client_secret\":\"KdhzQGTwrFongHpHutXt40YPKTi5CmIqeQ0bVgR54UvlvMPTrucW7SsCmSo1loSp\",\"audience\":\"blog\",\"grant_type\":\"client_credentials\"}"

    # headers = {'content-type': "application/json"}

    # conn.request("POST", "/oauth/token", payload, headers)

    # res = conn.getresponse()
    # data = res.read()

    # print(data.decode("utf-8"))


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True),
              'client_id': 'kfrmwrB4PMIsXz3ZxWl07tVNGejZQZgW'}
    return render_template('logout.html',
                           userinfo=None,
                           userinfo_pretty=None, indent=4)


@app.route('/dashboard')
@require_auth_from_session()
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='kfrmwrB4PMIsXz3ZxWl07tVNGejZQZgW',
    client_secret='EXS6SuDnxzclxF9qK_4BdgN58HsCxTPIiQ3HEvsNTDEGk2vczatJy-l3svPZwg4r',
    api_base_url='https://coffestack.us.auth0.com',
    access_token_url='https://coffestack.us.auth0.com/oauth/token',
    authorize_url='https://coffestack.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },


)

# /server.py

# Here we're using the /callback route.


@ app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'email': userinfo['email'],
        'picture': userinfo['picture'],
        'permission':'EDITOR' #default permission, need to change this later
    }
    print('session')
    print(session)

    #what's missing if we persist user obj (we don't need to do it now)
    """
    1. find user by session['profile']['name']
    2. if user does not exist, save user into User model/database
    sample code: 

    user = User.query.filter_by(email=userinfo['name']).first() 

    """

    # check if user already exists
    user = User.query.filter_by(username=userinfo['name']).first()
    """
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(20), unique=True, nullable=True)
        email = db.Column(db.String(120), unique=True, nullable=True)
        image_file = db.Column(db.String(20), nullable=True,
                               default='default.jpg')
        last_login_date = db.Column(db.DateTime, nullable=False)
        posts = db.relationship('Post', backref='author', lazy=True)

        def __repr__(self):
            return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    """
    if not user: # user does not exist in User model/table, therefore we create a record
        user = User(
            username=userinfo['name'],
            email=userinfo['name'],
            image_file = userinfo['picture'],
            last_login_date = datetime.datetime.now()
        )

        # insert the user
        db.session.add(user)
        db.session.commit()          

    else:  # user previously logged in before and created record before, we fetch that 
        #test
        print('--------user.id--------')
        print(user.id)
        #modify the user.last_lgoin_date with the datetime.datetime.now()
        user.last_lgoin_date = datetime.datetime.now()
        user.update()            
    return redirect('/')

def which_user():
    if session is None:
        return 'Guest'
    
    if 'profile' in session:
        profile = session['profile']
        user = User.query.filter_by(username=profile['name']).first()
        return user.id
    
    else:
        return 'Guest'
 

@app.route('/all-posts', methods=['GET'])
@require_auth_from_session()
def get_all_posts(token):
    try:
        posts = Post.query.all()
        posts_list = [str(post.title) for post in posts]

        return jsonify({
            'success': True, 
            'posts': posts_list,
        }), 200
    except:
        abort(500)

@app.route('/post/new', methods=['GET', 'POST'])
@require_auth_from_session()
def new_post():
    form = PostForm()
    user = which_user()
 
    if user == 'Guest':
        return redirect(url_for('login'))

    if form.validate_on_submit():
        # title = request.form['title']
        # content = request.form['content']

        #find user by session
        message = Post(title=form.title.data, content=form.content.data, user_id = user)
        db.session.add(message)
        db.session.commit()
        flash('Your Post Has Been Created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form, userinfo=session['profile'])


@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# @app.route('/post/<int:post_id>/update', methods=['POST'])
# @requires_auth('post:post')
# def patch_drink(jwt, post_id):


#     data = request.get_json()
#     title = data.get('title', None)

#     content = Post.query.filter_by(id=drink_id).one_or_none() #drink = Drink


#     if content is None: #drink
#         abort(404)

#     if title is None:
#         abort(400)

#     try:
#         content.title = title
#         content.update()

#         return jsonify({
#             'success': True,
#         })
#     except:
#         abort(422)

# @app.route('/post/<int:post_id>/update')
# @cross_origin(headers=["Content-Type", "Authorization"])
# @requires_auth('post:post')
# def update_post(jwt, post_id):
#     if session is None:
#         flash('Log in, please')
#         return redirect(url_for('home'))
#     # post=Post.query.get_or_404(post_id)
#     if session:
#         form=PostForm()
#         return render_template('create_post.html', title='Update Post', form=form, userinfo=session['profile'])





