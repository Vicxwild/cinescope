from utils.data_generator import DataGenerator

class TestAuth:
    def test_register_user(self, registered_user, test_user):
        response_data = registered_user

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"


    def test_register_and_login_user(self, api_manager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"


    def test_authenticate_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.authenticate(login_data)
        response_data = response.json()

        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"


    def test_login_user_with_invalid_credentials(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": DataGenerator.generate_random_password()
        }
        response = api_manager.auth_api.login_user(login_data, expected_status=401)
        response_data = response.json()

        assert "message" in response_data, "Отсутствует сообщение об ошибке"