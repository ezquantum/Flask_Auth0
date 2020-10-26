# FSND CAPSTONE: The Blog

## capstone project for Udacity

**Heroku link:** (https://sqt594.herokuapp.com/home)

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/flasktutorialactual` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in api.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Running the server

To run the server, execute:

```
export FLASK_APP=run.py
export FLASK_ENV=debug
flask run --reload
```


## Blog

This custom blog utilizes SESSION as well as AUTH0. As unusual a combination, this is meant to satisfy some requirements within the rubric. 

Unit-testing, though feasible isn't an easily approachable subject in regards to session. I have included a file that includes JSON testing IF auth0 functions were used. This will return a 401 due to configuration. This is a positive and passing test for these purposes. 

## Models

Author: Includes primary ID, username, email, optional image file, password, last login, and foreign key posts that communicates with the POST model. 

Models: Includes primary ID, title, date_posted, content of post as well as author ID foreign key

## Environment Variables

In the `.env` file, the JWT token for each User Role
- ADMIN
- User
x
## Roles

USER

GET | post | author | all-posts
POST| post | author |
PATCH| post|    
DELETE|post    

Admin
#####  All permissions plus "API endpoint"
API== Testable endpoint only

GET | post | author | all-posts | API
POST| post | author             | API
PATCH|post|                     | API
DELETE|post                     | API


Curling specific endpoints because they are not in JSON format will return HTML

`````bash
GET '/all-posts'

reponse = {
posts 
0 "ddd"
1 "zzz"
2 "dd"
success=true
  }


POST '/post/new'

1) Request for login from Curl
2) Return: HTML script with form data


PATCH '/post/<int:post_id>/update'

PARAMS = <int:post_id>

1) Request for login from Curl
2) Return: HTML script with form data



DELETE '/post/<int:post_id>/delete'

params = <int:post_id>

1) Request for login from Curl
2) Return: Check session for author ID matching current user ID
3) Delete occurs





GET '/login'

Redirect URL for AUTH0 login

response = {
<a href="https://coffestack.us.auth0.com/authorize?response_type=code&amp;client_id=kfrmwrB4PMIsXz3ZxWl07tVNGejZQZgW&amp;redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback&amp;scope=openid+profile+email&amp;state=3XIHBxl64S8qJFfZrHhGUq3CHTOb1T&amp;nonce=RC8oqU0ogycNGZCEJgMS">
https://coffestack.us.auth0.com/authorize?response_type=code&amp;client_id=kfrmwrB4PMIsXz3ZxWl07tVNGejZQZgW&amp;redirect_uri=http%3A%2F%2Flocalhost%3A5000%2Fcallback&amp;scope=openid+profile+email&amp;state=3XIHBxl64S8qJFfZrHhGUq3CHTOb1T&amp;nonce=RC8oqU0ogycNGZCEJgMS</a>


GET '/logout'

Logout
Redirects to homepage

`````
## Testing

To run the tests, cd into `/src` and run in your terminal

```bash

python test.py
`````

special thanks

The amazing mentors at udacity
Corey Schaffer for creating elaborate tutorials
My creative wife for all the help
