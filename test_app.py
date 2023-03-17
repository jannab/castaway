import os
import unittest
import json

from app import create_app
from models import Actor, Movie, db_drop_and_create_all


class CastAwayTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.database_name = "castaway_test"
        cls.database_path = "postgresql://{}/{}".format(
            '127.0.0.1:5432', cls.database_name)
        test_config = {"SQLALCHEMY_DATABASE_URI": cls.database_path}
        cls.app = create_app(test_config=test_config)
        cls.client = cls.app.test_client
        with cls.app.app_context():
            db_drop_and_create_all()

        cls.new_actor = {
            "name": "Kate Winslet",
            "age": 47,
            "gender": "female"
        }
        cls.new_movie = {
            "title": "Titanic",
            "releaseDate": "2019-03-25T15:59:22.403Z"
        }

    def test_01_create_actor(self):
        res = self.client().post("/actors/", json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_02_409_create_actor(self):
        res = self.client().post("/actors/", json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertTrue("error" in data)

    def test_03_404_get_actor_by_id(self):
        res = self.client().get("/actors/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_04_update_actor(self):
        res = self.client().patch("/actors/1", json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_05_delete_actor(self):
        res = self.client().delete("/actors/1")
        self.assertEqual(res.status_code, 204)

    def test_06_404_get_actor_by_id(self):
        res = self.client().get("/actors/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_07_404_update_actor(self):
        res = self.client().patch("/actors/1", json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_08_404_update_actor(self):
        res = self.client().patch("/actors/1", json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_09_404_delete_actor(self):
        res = self.client().delete("/actors/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_10_get_actors(self):
        res = self.client().get("/actors/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actors" in data)

    def test_11_405_get_actors(self):
        res = self.client().delete("/actors/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue("error" in data)

    def test_12_create_movie(self):
        res = self.client().post("/movies/", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_13_409_create_movie(self):
        res = self.client().post("/movies/", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertTrue("error" in data)

    def test_14_404_get_movie_by_id(self):
        res = self.client().get("/movies/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_15_update_movie(self):
        res = self.client().patch("/movies/1", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_16_delete_movie(self):
        res = self.client().delete("/movies/1")
        self.assertEqual(res.status_code, 204)

    def test_17_404_get_movie_by_id(self):
        res = self.client().get("/movies/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_18_404_update_movie(self):
        res = self.client().patch("/movies/1", json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_19_404_update_movie(self):
        res = self.client().patch("/movies/1", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_20_404_delete_movie(self):
        res = self.client().delete("/movies/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_21_get_movies(self):
        res = self.client().get("/movies/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movies" in data)

    def test_22_405_get_movies(self):
        res = self.client().delete("/movies/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue("error" in data)

if __name__ == "__main__":
    unittest.main()
