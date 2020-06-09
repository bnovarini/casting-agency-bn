import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class CastingAgencyCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagency_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Test actor',
            'age': 35,
            'gender': 'female',
        }

        self.new_movie = {
            'title': 'Test movie',
            'release_date': '2020-07-21T21:30:00.000Z',
        }

        self.assistant_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3ODE2YmZjY2EzMDAxOTdkNTVlMyIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2Njc1ODcsImV4cCI6MTU5MTc1Mzk4NywiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.T2HXWXWjVMJZ3-zsEmB77pnfL2yFZseS6L8bJ0OItL_uXZCsjmDQJNaEPWFZb0WYmZuiX9ncYtD9uCA-2SmuS6c9Q5aAG9-YZCfOG-7qYc3nbpjMjOBEoDA5W5WTechTXQsC39Sn4nbXv0NNE6ngUSRTwYP3VG7-5UwNFf0DeT78OtUB7gnDwiewmvWanPTj3gc1mT0YxPpdAdO0zy656YvrSpuayPq_SVKt-8vfUNgdrItCnQ8PQ9Q09UOrd9uUZ4OA95X3_NwrtA31n8UTWrwniptR_N70vcMcHM8Kf1rqatzvT4ZApW_NS-cH606jdYA50573w6bNaPcOO6iP8g'
        }

        self.director_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGI5MjI5ZGNlMDAxM2Q3OGVlZSIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2Njc2MjQsImV4cCI6MTU5MTc1NDAyNCwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDpjYXN0aW5ncyJdfQ.cywx4IY3WIizupnd2QSeHhniv0J7PhXonDV2ME4aEOLUFeC6iAt-jew1_sUVJrAprmOi59p31xbBmEm5dazMhhgsrKHdWL8pzFFncVV5rAaHiYfD8a7894SgW_AUw4CTkJu8PIiW-G4YinSfSqnttjYwaZ-jC_OW1fLKFcRlqSmqjpxB1iCEyRoYOwY2mS7gTzfT1VtthX4k872RSyROAy1Sowt_TcH9iav_f3W-BX305JYmXO16VBsKEo5lB4WEO9v5F9hklEwLh0h59MotksANRnwYTWXmgpuzuQLKE6zR8tTEhXYHZHPI9llLmwY5RhcQH_dBvdQ0uoADZ77ZVQ'
        }

        self.producer_header = {
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJxYlhjaTNBM0dtWDJtckQ4NEh0QSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYm4uYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZGQ3OGRlYmZjY2EzMDAxOTdkNTY3ZiIsImF1ZCI6ImNhc3RpbmdhZ2VuY3kiLCJpYXQiOjE1OTE2Njc2NTQsImV4cCI6MTU5MTc1NDA1NCwiYXpwIjoibmRBQTNJY2hTSHV4dG1oMllXaXl4bnBuaTJPRUFBakUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdGluZ3MiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6Y2FzdGluZ3MiLCJwb3N0Om1vdmllcyJdfQ.xlPOFztnBSiQYVUeonWZ5fE_F1FROCPG-2Jwrp-sSm0kSF7bPCEzehuZLUXBWe3Z8E26l66ljPGvd49xkWrxnFe5hfbh2HwR5o4NZz7KbY0c0D632e0y0X_01v_FrNy20Dz8H6nA5AwKEQh2tBaJ-kd5ZGHRL7urQQyXa3Q9t9uFGsXTVy4JkuAkI5aqA4bN1fTnqL9lYhP7UYdsBqlWTlNHFHKxSFgFdfZJfEVaJcgnq5lwYF8Jdc1lhU3nt8u5dG-nrC5h526yZmclA0QQyQxywKdeKpEChPa383rM_mYhItQSMNduQYe6nyBiy96pOXFfxBLLVahqSMie6w5eng'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # ACTOR TESTS

    def test_get_actors(self):
        """Test retrieving all actors"""
        res = self.client().get('/actors',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_no_auth(self):
        """Test retrieving all actors with no auth"""
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_actor(self):
        """Test retrieving specific actor"""
        res = self.client().get('/actors/10',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['id'], 10)

    def test_404_non_existent_actor(self):
        """Test retrieving non-existing actor"""
        res = self.client().get('/actors/100',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_new_actor_director(self):
        """Test adding a new actor with Director JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_producer(self):
        """Test adding a new actor with Producer JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_add_new_actor_assistant(self):
        """Test adding a new actor with Assistant JWT"""
        res = self.client().post('/actors',
                                 json=self.new_actor,
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_405_if_actor_creation_not_allowed(self):
        """Test adding an actor with wrong endpoint"""
        res = self.client().post('/actors/100',
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_actor_director(self):
        """Test modifying an actor with Director JWT"""
        res = self.client().patch('/actors/7',
                                  json=self.new_actor,
                                  headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 7)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_producer(self):
        """Test modifying an actor with Producer JWT"""
        res = self.client().patch('/actors/8',
                                  json=self.new_actor,
                                  headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['id'], 8)
        self.assertEqual(data['actor']['name'], self.new_actor['name'])

    def test_edit_actor_assistant(self):
        """Test modifying an actor with Assistant JWT"""
        res = self.client().patch('/actors/9',
                                  json=self.new_actor,
                                  headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_actor_producer(self):
        """Test deleting an actor with producer token"""
        res = self.client().delete('/actors/1',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '1')
        self.assertEqual(actor, None)

    def test_delete_actor_director(self):
        """Test deleting an actor with director token"""
        res = self.client().delete('/actors/2',
                                   headers=self.director_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(actor, None)

    def test_delete_actor_assistant(self):
        """Test deleting an actor with assistant token"""
        res = self.client().delete('/actors/3',
                                   headers=self.assistant_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(actor)

    # MOVIE TESTS

    def test_get_movies(self):
        """Test retrieving all movies"""
        res = self.client().get('/movies',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_no_auth(self):
        """Test retrieving all movies with no auth"""
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_movie(self):
        """Test retrieving specific movie"""
        res = self.client().get('/movies/10',
                                headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['id'], 10)

    def test_404_non_existent_movie(self):
        """Test retrieving non-existing movie"""
        res = self.client().get('/movies/100',
                                headers=self.assistant_header)
        self.assertEqual(res.status_code, 404)

    def test_add_new_movie_director(self):
        """Test adding a new movie with Director JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_add_new_movie_producer(self):
        """Test adding a new movie with Producer JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_add_new_movie_assistant(self):
        """Test adding a new movie with Assistant JWT"""
        res = self.client().post('/movies',
                                 json=self.new_movie,
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_405_if_movie_creation_not_allowed(self):
        """Test adding a movie with wrong endpoint"""
        res = self.client().post('/movies/100',
                                 json=self.new_actor)
        self.assertEqual(res.status_code, 405)

    def test_edit_movie_director(self):
        """Test modifying a movie with Director JWT"""
        res = self.client().patch('/movies/7',
                                  json=self.new_movie,
                                  headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 7)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_producer(self):
        """Test modifying a movie with Producer JWT"""
        res = self.client().patch('/movies/8',
                                  json=self.new_movie,
                                  headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 8)
        self.assertEqual(data['movie']['title'], self.new_movie['title'])

    def test_edit_movie_assistant(self):
        """Test modifying a movie with Assistant JWT"""
        res = self.client().patch('/movies/9',
                                  json=self.new_movie,
                                  headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie_director(self):
        """Test deleting a movie with director token"""
        res = self.client().delete('/movies/1',
                                   headers=self.director_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_delete_movie_producer(self):
        """Test deleting a movie with producer token"""
        res = self.client().delete('/movies/2',
                                   headers=self.producer_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(movie, None)

    def test_delete_movie_assistant(self):
        """Test deleting a movie with assistant token"""
        res = self.client().delete('/movies/3',
                                   headers=self.assistant_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
        self.assertTrue(movie)

    def test_add_new_movie_casting_director(self):
        """Test adding an actor casting to movie with Director JWT"""
        res = self.client().post('/movies/4/actors',
                                 json={'actor_id': 4},
                                 headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 4)

    def test_add_new_movie_casting_producer(self):
        """Test adding an actor casting to movie with Producer JWT"""
        res = self.client().post('/movies/5/actors',
                                 json={'actor_id': 6},
                                 headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['id'], 5)

    def test_add_new_movie_casting_assistant(self):
        """Test adding an actor casting to movie with Assistant JWT"""
        res = self.client().post('/movies/6/actors',
                                 json={'actor_id': 5},
                                 headers=self.assistant_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_non_existent_actor_for_casting(self):
        """Test retrieving non-existing actor for casting"""
        res = self.client().post('/movies/7/actors',
                                 json={'actor_id': 11},
                                 headers=self.producer_header)
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
