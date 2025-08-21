from faker import Faker
import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_CREDS
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager

faker = Faker()


@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user_with_delete(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]

    yield registered_user

    api_manager.user_api.clean_up_user(registered_user["id"])


@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    reg_user_ids = []

    def _create():
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        registered_user = test_user.copy()
        registered_user["id"] = response_data["id"]
        return registered_user

    yield _create()

    if "authorization" not in api_manager.session.headers:
        api_manager.auth_api.authenticate(ADMIN_CREDS)

    for user_id in reg_user_ids:
        api_manager.user_api.clean_up_user(user_id, expected_status=(200, 400, 404))

@pytest.fixture(scope="function")
def authenticated_admin(api_manager):
    response = api_manager.auth_api.authenticate(ADMIN_CREDS)
    return response


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)
