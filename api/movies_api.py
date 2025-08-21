from constants import CINESCOPE_URL, MOVIES
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=CINESCOPE_URL)

    def get_movies(self, page_size=None, page=None, min_price=None, max_price=None,
                   locations=None, published=None, genre_id=None, created_at=None, expected_status=200):
        params = {}

        if page_size is not None:
            params["pageSize"] = page_size
        if page is not None:
            params["page"] = page
        if min_price is not None:
            params["minPrice"] = min_price
        if max_price is not None:
            params["maxPrice"] = max_price
        if locations is not None:
            params["locations"] = locations
        if published is not None:
            params["published"] = published
        if genre_id is not None:
            params['genreId'] = genre_id
        if created_at is not None:
            params["createdAt"] = created_at

        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            params=params,
            expected_status=expected_status
        )

    def get_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint= f"{MOVIES}/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, movie_data, expected_status = 201):
        return self.send_request(
            method="POST",
            endpoint= MOVIES,
            data=movie_data,
            expected_status=expected_status
        )

    def update_movie(self, movie_id, updated_data, expected_status = 200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            data=updated_data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint= f"{MOVIES}/{movie_id}",
            expected_status=expected_status
        )
