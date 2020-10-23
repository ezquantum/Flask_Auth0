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
from flaskblogg.models import Author, Post, Guest, db, db_drop_and_create_all
from .auth import auth
from .auth.auth import AuthError, requires_auth_from_session, requires_auth, CLIENT_ID, CLIENT_SECRET, CLIENT_ID_TEST, CLIENT_SECRET_TEST, API_BASE_URL, AUTH0_DOMAIN, API_AUDIENCE
# from boto.s3.connection import S3Connection


# from flask_login import login_user

# CORS Headers 
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Paginates posts above five per page
# Reveals all posts
@app.route("/")
@app.route("/home")
def home():
    page=request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

# General about page
@app.route("/about")
def about():
    return render_template('about.html', title='About')

# native registration supported
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        author = Author(
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
            #'permission':'EDITOR'
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


# Auth0 redirect 
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://sqt594.herokuapp.com/callback')
    # return auth0.authorize_redirect(redirect_uri='http://localhost:5000/callback')

# clears session and adds redirect
@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True),
              'client_id': CLIENT_ID}
    return render_template('logout.html',
                           userinfo=None,
                           userinfo_pretty=None, indent=4)


 
#see the posts made from yourself
@app.route('/dashboard')
#see the posts made from that user
@app.route('/dashboard/<int:author_id>')
@requires_auth_from_session()
def dashboard(author_id = None):
    if author_id is not None:
        posts = Post.query.filter_by(author_id=author_id).all()
    else:
        author_id = get_author_id()
        posts = Post.query.filter_by(author_id=author_id).all()
    return render_template('dashboard.html',
                           posts = posts,
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_DOMAIN,
    client_secret=CLIENT_SECRET,
    api_base_url=API_BASE_URL,
    access_token_url=API_BASE_URL+'/oauth/token',
    authorize_url=API_BASE_URL+'/authorize',
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
        'author_id': userinfo['sub'],
        'name': userinfo['name'],
        'email': userinfo['email'],
        'picture': userinfo['picture'],
        #'permission':'EDITOR' #default permission, need to change this later
    }
    print(session)

    #what's missing if we persist user obj (we don't need to do it now)
    """
    1. find user by session['profile']['name']
    2. if user does not exist, save user into Author model/database
    sample code: 
    author = Author.query.filter_by(email=userinfo['name']).first() 
    """

    # check if user already exists
    author = Author.query.filter_by(username=userinfo['name']).first()

    if not author: # user does not exist in Author model/table, therefore we create a record
        author = Author(
            username=userinfo['name'],
            email=userinfo['name'],
            image_file = userinfo['picture'],
            last_login_date = datetime.datetime.now()
        )

        # insert the user
        db.session.add(author)
        db.session.commit()          

    else:  # user previously logged in before and created record before, we fetch that 
        #modify the user.last_lgoin_date with the datetime.datetime.now()
        author.last_login_date = datetime.datetime.now()
        author.update()            
    return redirect('/')




def get_author_id():
    guest = Guest()
    if session is None:
        return guest['id']
    
    if 'profile' in session:
        profile = session['profile']
        author = Author.query.filter_by(username=profile['name']).first()
        if author is not None:
            return author.id
        else:
            return guest['id']
    
    else:
        return guest['id']
 

#################### api with bear token  with method requires_auth #####################
################################## need to write test ###################################

# # # api demo endpoints
@app.route('/api/author/<int:author_id>/', methods=['GET','POST','PATCH'])
@requires_auth('patch:api') 
@cross_origin(headers=["Content-Type", "Authorization"])
@cross_origin(headers=["Access-Control-Allow-Origin", "https://sqt594.herokuapp.com"])
# @cross_origin(headers=["Access-Control-Allow-Origin", "http://localhost:5000"])

def api_get_all_posts_from_author(jwt, author_id):
    try:
        posts = Post.query.filter_by(author_id=author_id).all()
        posts_list = [str(post.title) for post in posts]

        return jsonify({
            'success': True, 
            'author_id':author_id,
            'posts': posts_list
        }), 200
    except:
        abort(422) 
# # # demo endpoint
@app.route('/api/post/<int:post_id>/remove', methods=['delete'])
@requires_auth('delete:api')
def delete_api(jwt, post_id):

    post = Post.query.get_or_404(post_id)
    author_id = get_author_id()

    if post is None:
        abort(403)

    if post.author_id !=  author_id:
        abort(403)
        # title = request.form['title']
        # content = request.form['content']

        #find author by session
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'danger')
    return redirect(url_for('home'))



################# end api with bear token  with method requires_auth ################## 


@app.route('/author/<int:author_id>/', methods=['GET'])
@requires_auth_from_session()
def get_all_posts_from_author(author_id):
    try:
        posts = Post.query.filter_by(author_id=author_id).all()
        posts_list = [str(post.title) for post in posts]

        return jsonify({
            'success': True, 
            'author_id':author_id,
            'posts': posts_list,
        }), 200
    except:
        abort(500)


@app.route('/all-posts', methods=['GET'])
@requires_auth_from_session()
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

# # # uses session to allow post
@app.route('/post/new', methods=['GET', 'POST'])
@requires_auth_from_session()
def new_post():
    form = PostForm()
    author_id = get_author_id()
    # guest id
    if author_id == -1:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        # title = request.form['title']
        # content = request.form['content']

        #find author by session
        message = Post(title=form.title.data, content=form.content.data, author_id = author_id)
        db.session.add(message)
        db.session.commit()
        flash('Your Post Has Been Created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post', userinfo=session['profile'])

# retrieve post by id: on clickable
@app.route('/post/<int:post_id>', methods=['GET'])
@requires_auth_from_session()
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

# # # Updates post
@app.route('/post/<int:post_id>/update', methods=['GET','POST'])
@requires_auth_from_session()
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    author_id = get_author_id()
    if post is None:
        abort(403)

    if post.author_id !=  author_id:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data  
        post.content = form.content.data
        db.session.commit()
        flash('Your Post Has Been Updated!', 'success')
        return redirect(url_for('post', post_id = post.id))
        
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', userinfo=session['profile'])


#Patch all Guest author's posts with author_id specified below
# @app.route('/patch-guest-author', methods=['PATCH'])
# @requires_auth()
# def patch_post(author_id):
#     guest = Guest()
#     post=Post.query.filter_by(author_id=guest.id).all()
    
#     if post is None:
#         return Response("There is no post under Guest author")

#     body = request.get_json()

#     try:
#         if 'author_id' in body:
#             author_id = body.get('author_id')

#             #validate if the author does exist in db
#             author = Author.query.get(author_id)

#             if author is not None:
#                 post.author_id = author_id
#                 post.update()
#                 return jsonify({
#                     'success': True,
#                 })
#             else:
#                 #author does not exit in the db
#                 abort(400)           

#     except: 
#         #author does not exit in body, malformed request
#         abort(400)


# @app.route('/post/<int:post_id>/delete', methods=['POST'])
# @requires_auth_from_session()
# def delete_post(post_id):
#     post=Post.query.get_or_404(post_id)
#     author_id = get_author_id()
#     if post is None:
#         abort(403)
#     if post.author_id !=  author_id:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash('Your Post Has Been deleted!', 'success')
#     return redirect(url_for('home'))


@app.route('/post/<int:post_id>/remove', methods=['GET', 'POST'])
@requires_auth_from_session()
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)
    author_id = get_author_id()

    if post is None:
        abort(403)

    if post.author_id !=  author_id:
        abort(403)
        # title = request.form['title']
        # content = request.form['content']

        #find author by session
    db.session.delete(post)
    db.session.commit()
    flash('Your Post Has Been Deleted!', 'danger')
    return redirect(url_for('home'))





@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                jsonify({
                        "success": False, 
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

@app.errorhandler(404)
def resource_not_found(error):

    return jsonify({
        "success": False,
        "error": 404,
        "message": "Page not found"
    }), 404

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above 
    '''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above 
    '''

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500

@app.errorhandler(AuthError)
def handle_auth_error(exception):
    response = jsonify(exception.error)
    response.status_code = exception.status_code
    return response









     
 
 