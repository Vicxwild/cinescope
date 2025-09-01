import random
from faker import Faker
faker = Faker()
import pytest


DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE = 1

@pytest.mark.api
class TestGet:
    def test_get_movie(self, unauthenticated_user, created_movie):
        get_resp = unauthenticated_user.api_manager.movies_api.get_movies()
        get_data = get_resp.json()

        assert get_resp.status_code == 200
        assert "movies" in get_data
        assert len(get_data["movies"]) == get_data["pageSize"] == DEFAULT_PAGE_SIZE
        assert get_data["page"] == DEFAULT_PAGE
        assert isinstance(get_data["movies"], list)

    def test_combined_filters(self, unauthenticated_user):
        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(
            min_price=100,
            max_price=500,
            locations=["MSK"],
            published=True,
            page_size=5
        )
        get_data = get_resp.json()

        assert get_resp.status_code == 200

        for movie in get_data["movies"]:
            assert 100 <= movie["price"] <= 500
            assert movie["location"] == "MSK"
            assert movie["published"] is True

    @pytest.mark.parametrize("min_max_prices,location,genre_id", [
        ((1, 1000), "MSK", 1),
        ((1, 1000), "SPB", 2),
        ((1, 1000), "MSK", 3)
    ], ids=["MSK 1", "SPB 2", "SPB 3"])
    def test_filters(self, min_max_prices, location, genre_id, unauthenticated_user):
        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(
            min_price=min_max_prices[0],
            max_price=min_max_prices[1],
            locations=[location],
            genre_id=genre_id
        )
        get_data = get_resp.json()

        assert get_resp.status_code == 200

        for movie in get_data["movies"]:
            assert min_max_prices[0] <= movie["price"] <= min_max_prices[1]
            assert movie["location"] == location
            assert movie["genreId"] == genre_id

    def test_with_page(self, unauthenticated_user, created_movie):
        random_page = faker.random_int(min=2, max=10)

        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(page=random_page)
        get_data = get_resp.json()

        assert get_resp.status_code == 200
        assert "movies" in get_data
        assert get_data["page"] == random_page

    def test_with_min_max_price(self, unauthenticated_user):
        random_min_price = faker.random_int(min=100, max=300)
        random_max_price = faker.random_int(min=400, max=600)

        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(min_price=random_min_price, max_price=random_max_price)
        get_data = get_resp.json()

        prices = [movie["price"] for movie in get_data["movies"]]

        assert get_resp.status_code == 200
        assert prices
        assert all(random_min_price <= price <= random_max_price for price in prices)

    def test_with_location(self, unauthenticated_user):
        rand_location = random.choice(["MSK", "SPB"])

        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(locations=[rand_location])
        get_data = get_resp.json()

        assert get_resp.status_code == 200

        locations = [movie["location"] for movie in get_data["movies"]]
        assert locations

        assert all(location == rand_location for location in locations)

    def test_negative_with_wrong_location(self, unauthenticated_user):
        rand_location = faker.word()

        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(locations=[rand_location], expected_status=400)
        get_data = get_resp.json()

        assert get_resp.status_code == 400
        assert get_data["message"]

    def test_negative_with_wrong_price(self, unauthenticated_user):
        random_price = faker.random_int(min=-1000, max=-300)

        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(min_price=random_price, expected_status=400)
        get_data = get_resp.json()

        assert get_resp.status_code == 400
        assert get_data["message"]

    def test_negative_with_zero_page(self, unauthenticated_user):
        get_resp = unauthenticated_user.api_manager.movies_api.get_movies(page=0, expected_status=400)
        get_data = get_resp.json()

        assert get_resp.status_code == 400
        assert get_data["message"]
