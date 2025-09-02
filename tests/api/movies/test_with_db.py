import datetime
import pytest
from db_requester.models import MovieDBModel
from utils.data_generator import DataGenerator
from pytz import timezone

@pytest.mark.db
class TestWithDB:
    def test_create_delete_movie(self, super_admin, db_session):
        movie_name = f"Test movie {DataGenerator.generate_random_str(10)}"

        films_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name).all()
        #проверяем что до начала тестирования фильма с таким названием нет
        assert len(films_from_db) == 0

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
        films_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name).all()
        assert len(films_from_db) == 1

        film_from_db = films_from_db[0]
        assert film_from_db.id == resp_json["id"]
        # можете обратить внимание что в базе данных етсь поле created_at которое мы не здавали явно
        # наш сервис сам его заполнил. проверим что он заполнил его верно с погрешностью в 5 минут
        assert film_from_db.created_at >= (datetime.datetime.now(timezone('UTC')).replace(tzinfo=None) - datetime.timedelta(minutes=5)), "Сервис выставил время создания с большой погрешностью"

        # Удаляем фильм
        super_admin.api_manager.movies_api.delete_movie(film_from_db.id)

        #проверяем что в конце тестирования фильма с таким названием действительно нет в базе
        films_from_db = db_session.query(MovieDBModel).filter(MovieDBModel.name == movie_name).all()
        assert len(films_from_db) == 0
