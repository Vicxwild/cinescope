from tests.api.helpers import get_id
import pytest

@pytest.mark.api
class TestPost:
    def test_create_movie(self, super_admin, created_movie, movie_test_data):
        post_data = created_movie

        assert "id" in post_data
        assert post_data["name"] == movie_test_data["name"]
        assert post_data["price"] == movie_test_data["price"]
        assert post_data["description"] == movie_test_data["description"]
        assert post_data["genreId"] == movie_test_data["genreId"]

        movie_id = get_id(post_data)

        get_resp = super_admin.api_manager.movies_api.get_movie(movie_id)
        get_data = get_resp.json()

        assert get_data["id"] == movie_id
        assert get_data["name"] == movie_test_data["name"]
        assert get_data["price"] == movie_test_data["price"]
        assert get_data["description"] == movie_test_data["description"]
        assert get_data["genreId"] == movie_test_data["genreId"]

    def test_negative_create_with_empty_data(self, super_admin):
        post_resp = super_admin.api_manager.movies_api.create_movie({}, expected_status=400)
        post_data = post_resp.json()

        assert post_resp.status_code == 400
        assert "message" in post_data

    def test_negative_create_with_empty_name(self, super_admin, movie_test_data):
        movie_test_data.update({"name": ""})
        post_resp = super_admin.api_manager.movies_api.create_movie(movie_test_data, expected_status=400)
        post_data = post_resp.json()

        assert post_resp.status_code == 400
        assert "message" in post_data

    def test_negative_create_without_permission(self, common_user, movie_test_data):
        post_resp = common_user.api_manager.movies_api.create_movie(movie_test_data, expected_status=403)
        post_data = post_resp.json()

        assert post_resp.status_code == 403
        assert "message" in post_data
