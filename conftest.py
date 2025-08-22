from faker import Faker
import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, ADMIN_CREDS
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager

faker = Faker()

created_user_ids = []

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
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]

    created_user_ids.append(registered_user["id"])

    return registered_user


@pytest.fixture(scope="session", autouse=True)
def cleanup_created_users(api_manager):
    yield

    api_manager.auth_api.authenticate(ADMIN_CREDS)

    for user_id in created_user_ids:
        api_manager.user_api.clean_up_user(user_id)


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
