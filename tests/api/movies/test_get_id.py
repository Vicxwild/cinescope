from tests.api.helpers import get_id
from faker import Faker
import pytest

faker = Faker()

@pytest.mark.api
class TestGetId:
    def test_get_movie(self, unauthenticated_user, created_movie, movie_test_data):
        movie_id = get_id(created_movie)

        get_resp = unauthenticated_user.api_manager.movies_api.get_movie(movie_id)
        get_data = get_resp.json()

        assert get_data["id"] == movie_id
        assert get_data["name"] == movie_test_data["name"]
        assert get_data["price"] == movie_test_data["price"]
        assert get_data["description"] == movie_test_data["description"]
        assert get_data["genreId"] == movie_test_data["genreId"]

    def test_negative_with_wrong_id(self, unauthenticated_user):
        movie_id = faker.random_int(min= 1_000_000, max=9_000_000)

        get_resp = unauthenticated_user.api_manager.movies_api.get_movie(movie_id, expected_status=404)
        get_data = get_resp.json()

        assert get_resp.status_code == 404
        assert "message" in get_data

    def test_negative_with_string_id(self, unauthenticated_user):
        movie_id = faker.word()

        get_resp = unauthenticated_user.api_manager.movies_api.get_movie(movie_id, expected_status=500)
        get_data = get_resp.json()

        assert get_resp.status_code == 500
        assert "message" in get_data


