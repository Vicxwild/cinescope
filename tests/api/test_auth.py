from utils.data_generator import DataGenerator
import pytest
from models.base_models import RegisterUserResponse, LoginUserResponse
from db_requester.models import UserDBModel

@pytest.mark.api
class TestAuth:
    def test_register_user(self, unauthenticated_user, registration_user_data):
        response = unauthenticated_user.api_manager.auth_api.register_user(registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == registration_user_data.email
        assert register_user_response.roles == registration_user_data.roles

    def test_register_user_db_session(self, unauthenticated_user, registration_user_data, db_session):
        response = unauthenticated_user.api_manager.auth_api.register_user(registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())

        users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id).all()
        assert len(users_from_db) == 1

        user_from_db = users_from_db[0]
        assert user_from_db.id == register_user_response.id
        assert user_from_db.email == register_user_response.email

    def test_register_and_login_user(self, unauthenticated_user, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }
        response = unauthenticated_user.api_manager.auth_api.login_user(login_data)
        response_data = response.json()
        login_user_response = LoginUserResponse(**response_data["user"])

        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert login_user_response.email == registered_user.email, "Email не совпадает"
        assert login_user_response.fullName == registered_user.fullName, "fullName не совпадает"


    def test_authenticate_user(self, unauthenticated_user, registered_user):
        login_data = (registered_user.email,registered_user.password)

        response = unauthenticated_user.api_manager.auth_api.authenticate(login_data)
        login_user_response = LoginUserResponse(**response.json()["user"])

        assert login_user_response.email == registered_user.email, "Email не совпадает"


    def test_login_user_with_invalid_credentials(self, unauthenticated_user, registered_user):
        login_data = {
            "email": registered_user.email,
            "password": DataGenerator.generate_random_password()
        }
        response = unauthenticated_user.api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"
