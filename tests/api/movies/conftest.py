import random
from faker import Faker
import pytest
from utils.data_generator import DataGenerator

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
def clean_up_created_movies(super_admin):
    yield

    if created_movie_ids:
        for movie_id in created_movie_ids:
            super_admin.api_manager.movies_api.clean_up_movie(movie_id)

