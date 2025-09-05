from custom_requester.custom_requester import CustomRequester
from constants.constants import BASE_URL

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_locator}", # id or email
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def update_user(self, user_id, updated_data, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=updated_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def clean_up_user(self, user_id, expected_status=(200, 401, 404)):
        self.delete_user(user_id, expected_status=expected_status)
