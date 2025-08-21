import random

from faker import Faker
import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_CREDS
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager

faker = Faker()

CREATED_MOVIES_IDS = []

@pytest.fixture(scope="function")
def movie_test_data():
    locations = ["MSK", "SPB"]
    genre_ids = list(range(1,11))

    return {
        "name": DataGenerator.generate_random_film_title(),
        "imageUrl": faker.url(),
        "price": faker.random_int(min=100, max=1000),
        "description": DataGenerator.generate_random_film_description(),
        "location": random.choice(locations),
        "published": random.choice([True, False]),
        "genreId": random.choice(genre_ids)
    }

@pytest.fixture(scope="function")
def movie_factory(api_manager, authenticated_admin, movie_test_data):
    created_ids = []

    def _create():
        payload = movie_test_data
        resp = api_manager.movies_api.create_movie(payload)
        data = resp.json()
        created_ids.append(data["id"])
        return data

    yield _create

    if "authorization" not in api_manager.session.headers:
        api_manager.auth_api.authenticate(ADMIN_CREDS)

    for movie_id in created_ids:
        api_manager.movies_api.delete_movie(movie_id, expected_status=(200, 400, 404))
