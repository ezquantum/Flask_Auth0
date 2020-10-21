
import unittest
import os
from flaskblogg import app
from models import db, Author, Post

#Restrict permissions from USER
#Allow user to read all, create post, delete own post, edit own post
#Allow Admin to read all, create post, delete own post, edit own post, delete anyone posts, restrict editing someone's post
# app = Flask(__name__)
# app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# database_name = "blogatog"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://Amajimoda@localhost:5432/blogatog'
# # db = SQLAlchemy(app)

database_path='postgres://Amajimoda@localhost:5432/blogatog'
User = os.getenv('User')
Admin = os.getenv('Admin')

#Load the environment containing role based restricted JWTs
load_dotenv()


def set_auth_header(role):
    if role == 'User':
        return {'Authorization': 'Bearer {}'.format(User)}
    elif role == 'Admin':
        return {'Authorization': 'Bearer {}'.format(Admin)}



class MainTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()




    # # blog endpoint tests

    def test_author_id(self):
        res = self.app.get(
            '/api/author/<int:author_id>/', headers=set_auth_header('User'))
        self.assertEqual(res.status_code, 200)

    def test_author_id(self):
        res = self.app.get(
            '/api/author/<int:author_id>/', headers=set_auth_header('Admin'))
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        res = self.app.get(
            '/api/post/<int:post_id>/delete', headers=set_auth_header('User'))
        self.assertEqual(res.status_code, 200)

    def test_delete(self):
        res = self.app.get(
            '/api/post/<int:post_id>/delete', headers=set_auth_header('Admin'))
        self.assertEqual(res.status_code, 200)



    # def test_register(self):
    #     res = self.app.get(
    #         '/register', headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 200)

    # def test_register(self):
    #     res = self.app.get(
    #         '/register', headers=set_auth_header('Admin'))
    #     self.assertEqual(res.status_code, 200)


    # def test_dashboard(self):
    #     res = self.app.get(
    #         '/dashboard', headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 200)

    # def test_dashboard(self):
    #     res = self.app.get(
    #         '/dashboard', headers=set_auth_header('Admin'))
    #     self.assertEqual(res.status_code, 200)




    # def test_get_movies_unauthorized(self):
    #     res = self.app.get(
    #         '/movies', headers=set_auth_header(''))
    #     self.assertEqual(res.status_code, 401)


    # def test_add_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }

    #     res = self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.get_json()['success'], True)



    # def test_add_movie_fail(self):
    #     res = self.app.post(
    #         '/movies', json={}, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res.get_json()['success'], False)



    # def test_add_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     res = self.app.post(
    #         '/movies', json=data, headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')



    # def test_edit_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)



    # def test_edit_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')



    # def test_edit_movie_fail(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post('/movies', json=data,
    #                   headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id

    #     data = {
    #         "title": '',
    #         "release_date": ''
    #     }
    #     res = self.app.patch(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)



    # def test_delete_movie(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.delete(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)




    # def test_delete_movie_unauthorized(self):
    #     data = {
    #         "title": "title",
    #         "release_date": "release_date"
    #     }
    #     self.app.post(
    #         '/movies', json=data, headers=set_auth_header('producer'))

    #     movie_id = Movie.query.first().id
    #     res = self.app.delete(
    #         f'/movies/{movie_id}', json=data,
    #         headers=set_auth_header('Admin'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')

    # # actors endpoint tests




    # def test_get_actors(self):
    #     res = self.app.get(
    #         '/actors', headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 200)




    # def test_get_actors_unauthorized(self):
    #     res = self.app.get(
    #         '/actors', headers=set_auth_header(''))
    #     self.assertEqual(res.status_code, 401)




    # def test_add_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     res = self.app.post(
    #         '/actors', json=data, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.get_json()['success'], True)




    # def test_add_actor_fail(self):
    #     res = self.app.post(
    #         '/actors', json={}, headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 400)
    #     self.assertEqual(res.get_json()['success'], False)




    # def test_add_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     res = self.app.post(
    #         '/actors', json=data, headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_edit_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)





    # def test_edit_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_edit_actor_fail(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.patch(
    #         f'/actors/{actor_id}', data={},
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)
    #     self.assertEqual(res.get_json()['message'], 'unauthorized')





    # def test_delete_actor(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.delete(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('producer'))
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(res.get_json()['success'], True)





    # def test_delete_actor_unauthorized(self):
    #     data = {
    #         "name": "name",
    #         "gender": "M"
    #     }
    #     self.app.post('/actors', json=data,
    #                   headers=set_auth_header('producer'))

    #     actor_id = Actor.query.first().id
    #     res = self.app.delete(
    #         f'/actors/{actor_id}', json=data,
    #         headers=set_auth_header('User'))
    #     self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()