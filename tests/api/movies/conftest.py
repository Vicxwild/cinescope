import random
from faker import Faker
import pytest
from utils.data_generator import DataGenerator
import requests
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles

faker = Faker()

created_movie_ids = []

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
def created_movie(super_admin, movie_test_data):
    payload = movie_test_data
    resp = super_admin.api_manager.movies_api.create_movie(payload)
    data = resp.json()
    created_movie_ids.append(data["id"])
    return data


@pytest.fixture(scope="session", autouse=True)
def clean_up_created_movies():
    yield

    if created_movie_ids:
        new_session = requests.Session()
        api_manager = ApiManager(new_session)

        super_admin = User(
            SuperAdminCreds.USERNAME,
            SuperAdminCreds.PASSWORD,
            list(Roles.SUPER_ADMIN.value),
            api_manager
        )

        super_admin.api_manager.auth_api.authenticate(super_admin.creds)
        for movie_id in created_movie_ids:
            super_admin.api_manager.movies_api.clean_up_movie(movie_id)

