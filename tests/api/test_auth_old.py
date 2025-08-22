import pytest
import requests
from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator

class TestAuth:
    @pytest.mark.skip(reason="Этот тест временно отключен")
    def test_register_user(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.post(register_url, json=test_user, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        # Проверки
        assert response.status_code == 201, "Ошибка регистрации пользователя"
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"

        # Проверяем, что роль USER назначена по умолчанию
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    @pytest.mark.skip(reason="Этот тест временно отключен")
    def test_login_success(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        reg_resp = requests.post(register_url, json=test_user, headers=HEADERS)
        assert reg_resp.status_code in [200, 201, 409], f"Регистрация не удалась: {reg_resp.status_code}, {reg_resp.text}"

        # Логируем ответ для диагностики
        print(f"Response status: {reg_resp.status_code}")
        print(f"Response body: {reg_resp.text}")

        # Логин юзера
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }

        login_resp = requests.post(login_url, json=login_data, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {login_resp.status_code}")
        print(f"Response body: {login_resp.text}")

        assert login_resp.status_code in [200,201], "Ошибка авторизации пользователя"
        data = login_resp.json()

        # Проверки токена
        access_token = data.get("accessToken")
        assert isinstance(access_token, str) and access_token.strip(), "Отсутствует токен доступа"

        # Проверки user
        user = data.get("user")
        assert isinstance(user, dict), "Отсутствует объект user в ответе"
        assert data["user"]["email"] == test_user["email"], "Имейл пользователя не совпадает"
        assert data["user"]["fullName"] == test_user["fullName"], "Полное имя пользователя не совпадает"

    @pytest.mark.skip(reason="Этот тест временно отключен")
    def test_login_with_wrong_password(self, test_user):
        # URL для регистрации
        register_url = f"{BASE_URL}{REGISTER_ENDPOINT}"

        # Отправка запроса на регистрацию
        reg_resp = requests.post(register_url, json=test_user, headers=HEADERS)
        assert reg_resp.status_code in [200, 201, 409], f"Регистрация не удалась: {reg_resp.status_code}, {reg_resp.text}"

        # Логируем ответ для диагностики
        print(f"Response status: {reg_resp.status_code}")
        print(f"Response body: {reg_resp.text}")

        # Логин юзера с неверным паролем
        login_url = f"{BASE_URL}{LOGIN_ENDPOINT}"
        wrong_password_data = {
            "email": test_user["email"],
            "password": DataGenerator.generate_random_password()
        }

        login_resp = requests.post(login_url, json=wrong_password_data, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {login_resp.status_code}")
        print(f"Response body: {login_resp.text}")

        assert login_resp.status_code in [401, 500], f"Ожидался 401/500 при неверном пароле, получено {login_resp.status_code}"
        assert "message" in login_resp.json(), "Отсутствует сообщение об ошибке"

        # Логин юзера с неверным паролем
        wrong_email_data = {
            "email": DataGenerator.generate_random_email(),
            "password": test_user["password"]
        }

        login_resp = requests.post(login_url, json=wrong_email_data, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {login_resp.status_code}")
        print(f"Response body: {login_resp.text}")

        assert login_resp.status_code in [401, 500], f"Ожидался 401/500 при неверном пароле, получено {login_resp.status_code}"
        assert "message" in login_resp.json(), "Отсутствует сообщение об ошибке"

        # Логин юзера с пустым телом запроса
        login_resp = requests.post(login_url, json={}, headers=HEADERS)

        # Логируем ответ для диагностики
        print(f"Response status: {login_resp.status_code}")
        print(f"Response body: {login_resp.text}")

        assert login_resp.status_code in [401, 500], "Пользователь вошел в свою учетную запись"
