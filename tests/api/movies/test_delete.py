from faker import Faker
from tests.api.helpers import get_id
import pytest
from db_requester.models import MovieDBModel

faker = Faker()

@pytest.mark.api
@pytest.mark.slow
class TestDelete:
    def test_delete_movie(self, super_admin, created_movie, db_session):
        movie_id = get_id(created_movie)

        movie_from_db = db_session.query(MovieDBModel).filter_by(id=movie_id).first()
        assert movie_from_db is not None
        assert movie_from_db.name == created_movie["name"]

        delete_resp = super_admin.api_manager.movies_api.delete_movie(movie_id, expected_status=200)
        assert delete_resp.status_code == 200

        movie_from_db = db_session.query(MovieDBModel).filter_by(id=movie_id).first()
        assert movie_from_db is None

    @pytest.mark.slow
    @pytest.mark.parametrize("user_fixture_name,status_code", [
        ("super_admin", 200),
        ("admin", 403),
        ("common_user", 403),
        ("unauthenticated_user", 401)
    ], ids=["super_admin - ok", "admin - forbidden", "common_user - forbidden", "unauthenticated_user - unauthorized"])
    def test_delete_with_parametrize(self, user_fixture_name, status_code, created_movie, request):
        movie_id = get_id(created_movie)

        user = request.getfixturevalue(user_fixture_name)

        user.api_manager.movies_api.delete_movie(movie_id, expected_status=status_code)

    def test_negative_with_wrong_id(self, super_admin):
        movie_id = faker.random_int(min= 1_000_000_000, max=9_000_000_000)
        delete_resp = super_admin.api_manager.movies_api.delete_movie(movie_id, expected_status=404)
        assert delete_resp.status_code == 404
