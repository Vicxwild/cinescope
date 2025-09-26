import datetime
import pytest
from db_models.movie import MovieDBModel
from utils.data_generator import DataGenerator
from pytz import timezone
from db_requester.db_helpers import DBHelper

@pytest.mark.db
class TestWithDB:
    def test_create_delete_movie(self, super_admin, db_session):
        movie_name = f"Test movie {DataGenerator.generate_random_str(10)}"
        db_helper = DBHelper(db_session)

        film_from_db = db_helper.get_movie_by_name(movie_name)
        #проверяем что до начала тестирования фильма с таким названием нет
        assert film_from_db is None

        created_movie_data = {
            "name": movie_name,
            "price": 500,
            "description": DataGenerator.generate_random_film_description(),
            "location": "MSK",
            "published": True,
            "genreId": 3
        }

        resp_json = super_admin.api_manager.movies_api.create_movie(created_movie_data).json()

        #проверяем после вызова api_manager.movies_api.create_movie в базе появился наш фильм
        film_from_db = db_helper.get_movie_by_name(movie_name)
        assert film_from_db is not None
        assert film_from_db.id == resp_json["id"]
        # можете обратить внимание что в базе данных етсь поле created_at которое мы не здавали явно
        # наш сервис сам его заполнил. проверим что он заполнил его верно с погрешностью в 5 минут
        assert film_from_db.created_at >= (datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(minutes=5)), "Сервис выставил время создания с большой погрешностью"

        # Удаляем фильм
        super_admin.api_manager.movies_api.delete_movie(film_from_db.id)

        #проверяем что в конце тестирования фильма с таким названием действительно нет в базе
        film_from_db = db_helper.get_movie_by_name(movie_name)
        assert film_from_db is None
