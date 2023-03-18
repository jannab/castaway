import os
import unittest
import json

from app import create_app
from models import Actor, Movie, db_drop_and_create_all

from dotenv import load_dotenv

load_dotenv()


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

        cls.ep_token = os.environ.get("EXECUTIVE_PRODUCER_TOKEN", "")
        cls.cd_token = os.environ.get("CASTING_DIRECTOR_TOKEN", "")
        cls.ca_token = os.environ.get("CASTING_ASSISTANT_TOKEN", "")
        cls.ep_headers = {"Authorization": "Bearer " + cls.ep_token}
        cls.cd_headers = {"Authorization": "Bearer " + cls.cd_token}
        cls.ca_headers = {"Authorization": "Bearer " + cls.ca_token}
        cls.missing_bearer_headers = {"Authorization": cls.ca_token}
        cls.no_bearer_token_headers = {"Authorization": "No Bearer Token"}
        cls.malformed_bearer_headers = {"Authorization": "Bearer Malformed"}

        cls.new_actor_1 = {
            "name": "Kate Winslet",
            "age": 47,
            "gender": "female"
        }
        cls.new_actor_2 = {
            "name": "Leonardo DiCaprio",
            "age": 48,
            "gender": "male"
        }
        cls.new_movie = {
            "title": "Titanic",
            "releaseDate": "2019-03-25T15:59:22.403Z"
        }

    def test_01_401_no_auth_create_actor(self):
        res = self.client().post("/actors/",
                                 json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_02_401_missing_bearer_create_actor(self):
        res = self.client().post("/actors/",
                                 json={},
                                 headers=self.missing_bearer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_03_401_no_bearer_token_create_actor(self):
        res = self.client().post("/actors/",
                                 json={},
                                 headers=self.no_bearer_token_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_04_401_malformed_bearer_create_actor(self):
        res = self.client().post("/actors/",
                                 json={},
                                 headers=self.malformed_bearer_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertTrue("error" in data)

    def test_05_create_actor_role_ep(self):
        res = self.client().post("/actors/",
                                 json=self.new_actor_1,
                                 headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_06_409_create_actor_role_ep(self):
        res = self.client().post("/actors/",
                                 json=self.new_actor_1,
                                 headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertTrue("error" in data)

    def test_07_create_actor_role_cd(self):
        res = self.client().post("/actors/",
                                 json=self.new_actor_2,
                                 headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_08_403_create_actor_role_ca(self):
        res = self.client().post("/actors/",
                                 json={},
                                 headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_09_401_no_auth_get_actor_by_id(self):
        res = self.client().get("/actors/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_10_404_get_actor_by_id_role_ep(self):
        res = self.client().get("/actors/100", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_11_get_actor_by_id_role_ep(self):
        res = self.client().get("/actors/1", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_12_get_actor_by_id_role_ep(self):
        res = self.client().get("/actors/1", headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_13_get_actor_by_id_role_ep(self):
        res = self.client().get("/actors/1", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_14_401_no_auth_update_actor_by_id(self):
        res = self.client().patch("/actors/1",
                                  json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_15_404_update_actor_by_id_role_ep(self):
        res = self.client().patch("/actors/100",
                                  json={},
                                  headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_16_update_actor_by_id_role_ep(self):
        res = self.client().patch("/actors/1",
                                  json=self.new_actor_1,
                                  headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_17_update_actor_by_id_role_cd(self):
        res = self.client().patch("/actors/1",
                                  json=self.new_actor_1,
                                  headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actor" in data)

    def test_18_403_update_actor_by_id_role_ca(self):
        res = self.client().patch("/actors/1",
                                  json={},
                                  headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_19_401_no_auth_get_actors(self):
        res = self.client().get("/actors/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_20_405_wrong_method_get_actors_role_ep(self):
        res = self.client().delete("/actors/", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue("error" in data)

    def test_21_get_actors_role_ep(self):
        res = self.client().get("/actors/", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actors" in data)

    def test_22_get_actors_role_cd(self):
        res = self.client().get("/actors/", headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actors" in data)

    def test_23_get_actors_role_ca(self):
        res = self.client().get("/actors/", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("actors" in data)

    def test_24_401_no_auth_delete_actor_by_id(self):
        res = self.client().delete("/actors/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_25_404_delete_actor_role_ep(self):
        res = self.client().delete("/actors/100", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_26_delete_actor_role_ep(self):
        res = self.client().delete("/actors/1", headers=self.ep_headers)
        self.assertEqual(res.status_code, 204)

    def test_27_delete_actor_role_cd(self):
        res = self.client().delete("/actors/2", headers=self.cd_headers)
        self.assertEqual(res.status_code, 204)

    def test_28_403_delete_actor_role_ca(self):
        res = self.client().delete("/actors/100", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_29_401_no_auth_create_movie(self):
        res = self.client().post("/movies/", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_30_create_movie_role_ep(self):
        res = self.client().post("/movies/",
                                 json=self.new_movie,
                                 headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_31_409_create_movie_role_ep(self):
        res = self.client().post("/movies/",
                                 json=self.new_movie,
                                 headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 409)
        self.assertTrue("error" in data)

    def test_32_403_create_movie_role_cd(self):
        res = self.client().post("/movies/",
                                 json={},
                                 headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_33_403_create_movie_role_ca(self):
        res = self.client().post("/movies/",
                                 json={},
                                 headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_34_401_no_auth_get_movie_by_id(self):
        res = self.client().get("/movies/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_35_404_get_movie_by_id_role_ep(self):
        res = self.client().get("/movies/100", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_36_get_movie_by_id_role_ep(self):
        res = self.client().get("/movies/1", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_37_get_movie_by_id_role_cd(self):
        res = self.client().get("/movies/1", headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_38_get_movie_by_id_role_ca(self):
        res = self.client().get("/movies/1", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_39_401_no_auth_update_movie_by_id(self):
        res = self.client().patch("/movies/1", json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_40_404_update_movie_role_ep(self):
        res = self.client().patch("/movies/100",
                                  json={},
                                  headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_41_update_movie_role_ep(self):
        res = self.client().patch("/movies/1",
                                  json=self.new_movie,
                                  headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_42_update_movie_role_cd(self):
        res = self.client().patch("/movies/1",
                                  json=self.new_movie,
                                  headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movie" in data)

    def test_43_403_update_movie_role_ca(self):
        res = self.client().patch("/movies/1",
                                  json=self.new_movie,
                                  headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_44_401_no_auth_get_movies(self):
        res = self.client().get("/movies/")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_45_405_wrong_method_get_movies_role_ep(self):
        res = self.client().delete("/movies/", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertTrue("error" in data)

    def test_46_get_movies_role_ep(self):
        res = self.client().get("/movies/", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movies" in data)

    def test_47_get_movies_role_cd(self):
        res = self.client().get("/movies/", headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movies" in data)

    def test_48_get_movies_role_ca(self):
        res = self.client().get("/movies/", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue("movies" in data)

    def test_49_401_no_auth_delete_movie_by_id(self):
        res = self.client().delete("/movies/1")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertTrue("error" in data)

    def test_50_404_delete_movie_role_ep(self):
        res = self.client().delete("/movies/100", headers=self.ep_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertTrue("error" in data)

    def test_51_delete_movie_role_ep(self):
        res = self.client().delete("/movies/1", headers=self.ep_headers)
        self.assertEqual(res.status_code, 204)

    def test_52_403_delete_movie_role_cd(self):
        res = self.client().delete("/movies/100", headers=self.cd_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)

    def test_53_403_delete_movie_role_ca(self):
        res = self.client().delete("/movies/100", headers=self.ca_headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertTrue("error" in data)


if __name__ == "__main__":
    unittest.main()
