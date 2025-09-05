from utils.data_generator import DataGenerator
import pytest
from models.base_models import RegisterUserResponse, LoginUserResponse
from db_requester.models import UserDBModel
from constants.roles import Roles
import datetime
import allure
from pytest_check import check

@pytest.mark.api
@allure.label("qa_name", "Ivan Petrovich")
@allure.severity(allure.severity_level.MINOR)
class TestAuth:
    @allure.title("Тест регистрации пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_user(self, unauthenticated_user, registration_user_data):
        with allure.step("Выполнение запроса"):
            response = unauthenticated_user.api_manager.auth_api.register_user(registration_user_data)

        with allure.step("Извлекаем данные"):
            register_user_response = RegisterUserResponse(**response.json())

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with check:
                assert register_user_response.email == registration_user_data.email
                assert register_user_response.roles == registration_user_data.roles

    @allure.title("Test of registration with db")
    def test_register_user_db_session(self, unauthenticated_user, registration_user_data, db_session):
        with allure.step("Request"):
            response = unauthenticated_user.api_manager.auth_api.register_user(registration_user_data)

        with allure.step("Retrieving data from request"):
            register_user_response = RegisterUserResponse(**response.json())

        with allure.step("Retrieving data from db"):
            users_from_db = db_session.query(UserDBModel).filter(UserDBModel.id == register_user_response.id).all()

        with check("Checking for a single user"):
            assert len(users_from_db) == 1

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with check:
                user_from_db = users_from_db[0]
                check.equal(user_from_db.id, register_user_response.id)
                check.equal(user_from_db.email, register_user_response.email)

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    def test_register_user_mock(self, unauthenticated_user, test_user, mocker):
        with allure.step("Мокаем метод register_user в auth_api"):
            # Фиктивный ответ
            mock_response = RegisterUserResponse(
                    id = "id",
                    email = "email@email.com",
                    fullName = "fullName",
                    verified = True,
                    banned = False,
                    roles = [Roles.SUPER_ADMIN],
                    createdAt = str(datetime.datetime.now())
                )

        mocker.patch.object(
            unauthenticated_user.api_manager.auth_api,  # Объект, который нужно замокать
            "register_user",                            # Метод, который нужно замокать
            return_value=mock_response                  # Фиктивный ответ
        )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = unauthenticated_user.api_manager.auth_api.register_user(test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with allure.step("Проверка поля персональных данных"): #обратите внимание на вложенность allure.step
                with check:
                    #Строка ниже выдаст исключение, но выполнение теста продолжится
                    # check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email, mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):  # можно использовать вместо allure.step
                    check.equal(register_user_response.banned, mock_response.banned)

    @allure.title("Test of registration and auth")
    def test_register_and_login_user(self, unauthenticated_user, registered_user):
        with allure.step("Preparing data"):
            login_data = {
                "email": registered_user.email,
                "password": registered_user.password
            }

        with allure.step("Request"):
            response = unauthenticated_user.api_manager.auth_api.login_user(login_data)

        with allure.step("Retrieving data from request"):
            response_data = response.json()
            login_user_response = LoginUserResponse(**response_data["user"])

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with check:
                assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
                assert login_user_response.email == registered_user.email, "Email не совпадает"
                assert login_user_response.fullName == registered_user.fullName, "fullName не совпадает"


    @allure.title("Test of auth")
    def test_authenticate_user(self, unauthenticated_user, registered_user):
        with allure.step("Request"):
            login_data = (registered_user.email,registered_user.password)

        with allure.step("Retrieving data from request"):
            response = unauthenticated_user.api_manager.auth_api.authenticate(login_data)
            login_user_response = LoginUserResponse(**response.json()["user"])

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            with check:
                assert login_user_response.email == registered_user.email, "Email не совпадает"

    @allure.title("Test of login user with invalid credentials")
    def test_login_user_with_invalid_credentials(self, unauthenticated_user, registered_user):
        with allure.step("Preparing data"):

            login_data = {
                "email": registered_user.email,
                "password": DataGenerator.generate_random_password()
            }

        with allure.step("Request"):
            response = unauthenticated_user.api_manager.auth_api.login_user(login_data, expected_status=401)

        with allure.step("Retrieving data from request"):
            response_data = response.json()

        with allure.step("Checking for an error message"):
            assert "message" in response_data, "Отсутствует сообщение об ошибке"
