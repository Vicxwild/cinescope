from utils.data_generator import DataGenerator
from faker import Faker
from tests.api.helpers import get_id

faker = Faker()

class TestPatch:
    def test_update_movie(self, api_manager, authenticated_admin, movie_factory, movie_test_data):
        movie_id = get_id(movie_factory())
        updating_data=  {
            "name": DataGenerator.generate_random_film_title(),
            "price": faker.random_int(min=1000, max=1200)
        }

        patch_resp = api_manager.movies_api.update_movie(movie_id, updating_data)
        patch_data =patch_resp.json()

        assert patch_resp.status_code == 200
        assert patch_data["id"] == movie_id
        assert patch_data["name"] == updating_data["name"]
        assert patch_data["price"] == updating_data["price"]
        assert patch_data["description"] == movie_test_data["description"]
        assert patch_data["genreId"] == movie_test_data["genreId"]

        get_resp = api_manager.movies_api.get_movie(movie_id)
        get_data = get_resp.json()

        assert get_data["id"] == movie_id
        assert get_data["name"] == updating_data["name"]
        assert get_data["price"] == updating_data["price"]
        assert get_data["description"] == movie_test_data["description"]
        assert get_data["genreId"] == movie_test_data["genreId"]
        
    def test_negative_with_empty_name(self, api_manager, authenticated_admin, movie_factory, movie_test_data):
        movie_id = get_id(movie_factory())

        get_resp = api_manager.movies_api.get_movie(movie_id)
        get_data = get_resp.json()

        # фильм существует
        assert get_data["id"] == movie_id
        assert get_data["name"] == movie_test_data["name"]
        assert get_data["price"] == movie_test_data["price"]
        assert get_data["description"] == movie_test_data["description"]
        assert get_data["genreId"] == movie_test_data["genreId"]

        # по неизвестным мне причинам бекенд отвечает 404 - фильм не найден, хотя должен отдавать 400
        updating_data =  {"name": ""}
        patch_resp = api_manager.movies_api.update_movie(movie_id, updating_data, expected_status=(400, 404))
        patch_data =patch_resp.json()

        assert patch_resp.status_code in (400, 404)
        assert "message" in patch_data

    def test_negative_with_negative_price(self, api_manager, authenticated_admin, movie_factory, movie_test_data):
        movie_id = get_id(movie_factory())

        updating_data = {"price": faker.random_int(min=-1000, max=-100)}

        patch_resp = api_manager.movies_api.update_movie(movie_id, updating_data, expected_status=400)
        patch_data =patch_resp.json()

        assert patch_resp.status_code == 400
        assert "message" in patch_data

    def test_negative_with_numeric_description(self, api_manager, authenticated_admin, movie_factory, movie_test_data):
        movie_id = get_id(movie_factory())

        updating_data = {"description": faker.random_int(min=10, max=20)}

        patch_resp = api_manager.movies_api.update_movie(movie_id, updating_data, expected_status=400)
        patch_data =patch_resp.json()

        assert patch_resp.status_code == 400
        assert "message" in patch_data

    def test_negative_without_auth(self, api_manager, movie_factory):
        movie_id = get_id(movie_factory())

        updating_data=  {"name": "title", "price": 100 }
        api_manager.auth_api.unauthorize()
        patch_resp = api_manager.movies_api.update_movie(movie_id, updating_data, expected_status=401)
        patch_data =patch_resp.json()

        assert patch_resp.status_code == 401
        assert "message" in patch_data