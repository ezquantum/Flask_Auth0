from urllib.request import urlopen
from flask import request, _request_ctx_stack, abort, Flask, jsonify, render_template, url_for, flash, session, redirect, g
from six.moves.urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import HTTPException
from os import environ as env
from flaskblogg import app
import json
from functools import wraps
from flaskblogg.forms import RegistrationForm, LoginForm, PostForm
from jose import jwt
from flaskblogg.models import User, Post
from .auth import auth
from .auth.auth import requires_auth, AuthError
# from flaskblog.auth import AuthError, requires_auth

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

# native registration supported


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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


@ app.route('/dashboard')
@ auth.requires_auth()
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
        'picture': userinfo['picture']
    }
    print('session')
    print(session)

    # print(session['profile'])
    return redirect('/')

#############################


@app.route('/post/new', methods=['GET', 'POST'])
# @auth.requires_auth()
def new_post():

    form = PostForm()

    title = request.form['title']
    content = request.form['content']
    if session is None:
        flash('Your need to login', 'error')
        return redirect(url_for('home'))
    if form.validate_on_submit():
        flash('Your Post has been Created!', 'success')
        new_content = Post(title=title, content=content)
        db.session.add(new_content)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, userinfo=session['profile'])
#############
