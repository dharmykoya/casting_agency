
import unittest
import json

from app import APP
from database.models import Movie, Actor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.casting_assistant = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56VXlNek00T0RrMVJqRTRRVVk0T0RFMU56QTJNRGd5TkRGRlJUSXhORFk0UTBVMU5UazVNZyJ9.eyJpc3MiOiJodHRwczovL2RhbWlrb3lhLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTI2ZTI1MTc1ODdkNDBjYzNlMjg2YjciLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTc5NjA3MTgzLCJleHAiOjE1Nzk2MTQzODMsImF6cCI6IklaUnIzdDFOZzRnV29iZkxZeUhCSFVEcjFEbUJkZkFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.IAch5cu7PhKzpVm6Ultq5Z7_dB-ju5ZzB5RNpBFC71LyK0OUUdKKmWSrzUNfHUQZUv2CHigDDQZtlZojI-_xCibTYawYYKxvR_IwOuZSTA-QbJMkTgnT_i773JTy1x5lI4SHCegSn0A1_-ZaUkqMiHVwKjLdH0KL9bJX-z6gSCyO0gxdjrdrAqcdBFI1u9Xj8DiO25q6DmUL3kx5Kyj8DrE_zWk02sjP542Jknzm0UPQ3Dk7C5SHQAyis9dtqV0sfXhMlmK6ku8gTDokTbZWPO52pN8nAnpWo8MmbtdmkuU1SNcpB2Ru-xhfUPadbhAGfFPSupRIeaxghOlZXZfDYA'
        self.casting_director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56VXlNek00T0RrMVJqRTRRVVk0T0RFMU56QTJNRGd5TkRGRlJUSXhORFk0UTBVMU5UazVNZyJ9.eyJpc3MiOiJodHRwczovL2RhbWlrb3lhLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTI2ZTU4MWViZjY4MTBlYTZkMjViNWIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTc5NjA3NjMzLCJleHAiOjE1Nzk2MTQ4MzMsImF6cCI6IklaUnIzdDFOZzRnV29iZkxZeUhCSFVEcjFEbUJkZkFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJ1cGRhdGU6YWN0b3IiLCJ1cGRhdGU6bW92aWUnIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.OXL4QcHjHUI2dhhEWrr3sgCVenjNS6dnuT73qTKFH7ExAp2zIh5_y2VoPmQzLhRfADUpIqHOSFiif3JHukPVfTA26vFr8Zi0-wA9Gay32VlURNjil_rB4rrpqCUhS6IJZRcNh64jmTxmNlNspTdunti2idOG4wPa7J_H3EdtVOsD7T2TTlfcKDGQTgm0QDoMOJTcZi7raHeKxXdrfi0jE5r1hGRXwdOk9bqDba6D79VGcsDYLTJPj4FawSjAZSqHM500n5sSnyKyhpC4poMNVQfaYMteY4dvxlgkg_NTtNjJt9Fbf_EEOM1pVGnJ8Wz7cf0pd723dHr7pHWrGLijeQ'
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56VXlNek00T0RrMVJqRTRRVVk0T0RFMU56QTJNRGd5TkRGRlJUSXhORFk0UTBVMU5UazVNZyJ9.eyJpc3MiOiJodHRwczovL2RhbWlrb3lhLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTI2ZTcyOTRhY2JiMjBlYjc4NWExYjIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTc5NjA4MDQ2LCJleHAiOjE1Nzk2MTUyNDYsImF6cCI6IklaUnIzdDFOZzRnV29iZkxZeUhCSFVEcjFEbUJkZkFVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6bW92aWUnIiwiY3JlYXRlOmFjdG9yIiwiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllJyIsInVwZGF0ZTphY3RvciIsInVwZGF0ZTptb3ZpZSciLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.UJd6AN4hr-XfKZGb8WgMZhcHYh8Cd_sNvQjAP7sNU8jOrsPJeAWV8eYhX1z4205a5YQiQlrjm_CxX6EL-ckrNGa-hhp9Zl6GzNmtoXTHFFsmZ-2S_tyLvlRSeUauAriWO-_hlfsz3A54BH9aYIoYFT6eV0sdWcIA-og7IJ5wvDD4m8zKRic8SVtdsl4Q5LZkv-hB-9gARF_HfW5TV99LIthhHnZ2wzBvVLgIdoIjL9CzaChRzmoU1zoTR2dvQ8g5MqgAwd9bNcNfGfKdT3Bm-qe9t_BXmPVcv5lnR7E0A-K9OGXmxHjoj1NM08I5w3Sd6XPNtMgFY2pGMBDPgFDekQ'

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_create_actor_with_casting_assistant_token(self):
        payload = {
            'name': 'Damilola',
            'gender': 'male',
            'age': 29
        }
        response = self.client().post(
            '/actors',
            json=payload, headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(response.status_code, 401)

    def test_create_movie_with_casting_director_token(self):
        payload = {
            'title': 'Oleku',
            'release_date': '17th December 2019'
        }
        response = self.client().post(
            '/movies',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            })
        self.assertEqual(response.status_code, 401)

    def test_create_movie_with_casting_assistant_token(self):
        payload = {
            'title': 'Power',
            'release_date': '2nd Deecember 2019'
        }
        response = self.client().post(
            '/movies',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(response.status_code, 401)

    def test_create_actor(self):
        payload = {
            'name': 'Sewa',
            'gender': 'femal',
            'age': 25
        }
        response = self.client().post(
            '/actors',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            })
        self.assertEqual(response.status_code, 200)

    def test_create_movie(self):
        payload = {
            'title': 'Legends',
            'release_date': '14th Janaury 2019'
        }
        response = self.client().post(
            '/movies',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_token)
            })
        self.assertEqual(response.status_code, 200)

    def test_update_actor_with_casting_assistant_token(self):
        payload = {
            'name': 'Tolumide',
            'gender': 'female',
            'age': 19
        }
        response = self.client().patch(
            '/actors/1',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(response.status_code, 401)

    def test_update_movie_with_casting_assistant_token(self):
        payload = {
            'release_date': '14th November 2019'
        }
        response = self.client().patch(
            '/movies/1',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(response.status_code, 401)

    def test_update_actor(self):
        payload = {
            'name': 'Tolumide',
            'gender': 'female',
            'age': 19
        }
        response = self.client().patch(
            '/actors/1',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_token)
            })
        self.assertEqual(response.status_code, 200)

    def test_update_movie(self):
        payload = {
            'release_date': '17th June 2019'
        }
        response = self.client().patch(
            '/movies/1',
            json=payload,
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_token)
            })
        self.assertEqual(response.status_code, 200)

    def test_delete_actor_with_casting_assistant_token(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_with_casting_assistant_token(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant)
            })
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_with_casting_director_token(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director)
            })
        self.assertEqual(res.status_code, 401)

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_token)
            })
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
