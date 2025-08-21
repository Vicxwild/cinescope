from constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT, BASE_URL
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    # Клас для работы с аутентификацией

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def register_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=200):
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds["email"],
            "password": user_creds["password"]
        }

        response = self.login_user(login_data)
        response_data = response.json()
        if "accessToken" not in response_data:
            raise KeyError("access token missing")

        token = response_data["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})

        return response

    def unauthorize(self):
        self._delete_session_headers("authorization")

