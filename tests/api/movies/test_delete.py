from faker import Faker
from tests.api.helpers import get_id

faker = Faker()

class TestDelete:
    def test_delete_movie(self, api_manager, authenticated_admin, created_movie):
        movie_id = get_id(created_movie)

        delete_resp = api_manager.movies_api.delete_movie(movie_id, expected_status=200)
        assert delete_resp.status_code == 200

        get_resp = api_manager.movies_api.get_movie(movie_id, expected_status=404)
        assert get_resp.status_code == 404

    def test_negative_with_wrong_id(self, api_manager, authenticated_admin):
        movie_id = faker.random_int(min= 1_000_000_000, max=9_000_000_000)
        delete_resp = api_manager.movies_api.delete_movie(movie_id, expected_status=404)
        assert delete_resp.status_code == 404

    def test_negative_without_auth(self, api_manager, created_movie):
        movie_id = get_id(created_movie)

        api_manager.auth_api.unauthorize()

        delete_resp = api_manager.movies_api.delete_movie(movie_id, expected_status=401)
        assert delete_resp.status_code == 401