import time

from faker import Faker
import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from resources.user_creds import SuperAdminCreds
from resources.db_creds import DBCreds
from entities.user import User
from constants.roles import Roles
from models.base_models import TestUser

faker = Faker()

created_user_ids = []

@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER]
    }

@pytest.fixture(scope="function")
def registration_user_data(test_user: dict) -> TestUser:
    return TestUser(**test_user)

@pytest.fixture(scope="function")
def creation_user_data(test_user: dict) -> TestUser:
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })

    return TestUser(**updated_data)

@pytest.fixture(scope="function")
def registered_user(unauthenticated_user, registration_user_data: TestUser) -> TestUser:
    response = unauthenticated_user.api_manager.auth_api.register_user(registration_user_data)
    response_data = response.json()

    registered_user = registration_user_data.model_copy(update={"id": response_data["id"]})
    created_user_ids.append(registered_user.id)

    return registered_user


@pytest.fixture(scope="session", autouse=True)
def cleanup_created_users(super_admin):
    yield

    if created_user_ids:
        for user_id in created_user_ids:
            super_admin.api_manager.user_api.clean_up_user(user_id)


@pytest.fixture(scope="session")
def user_session():
    user_session_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_session_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user_sess in user_session_pool:
        user_sess.close_session()


@pytest.fixture(scope="function")
def unauthenticated_user(user_session):
    session = user_session()

    return User(
        "unauthenticated_user",
       "unauthenticated_user",
        ["PUBLIC"],
        session
    )


@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        list(Roles.USER.value),
        new_session
    )

    super_admin.api_manager.user_api.create_user(creation_user_data)
    common_user.api_manager.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="session")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        list(Roles.SUPER_ADMIN.value),
        new_session
    )

    super_admin.api_manager.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="session")
def admin(user_session, super_admin):
    admin_session = user_session()

    random_password = DataGenerator.generate_random_password()
    creation_admin_data = {
        "email": f"ADMIN_{DataGenerator.generate_random_email()}",
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.ADMIN.value],
        "verified": True,
        "banned": False
    }

    admin = User(
        creation_admin_data["email"],
        creation_admin_data["password"],
        [Roles.ADMIN.value],
        admin_session
    )

    admin_data = super_admin.api_manager.user_api.create_user(creation_admin_data).json()
    # ошибка в логике бэка - при создании пользователя с админской ролью создается юзер, для этого приходится патчить
    super_admin.api_manager.user_api.update_user(admin_data["id"], {"roles": [Roles.ADMIN.value]})
    admin.api_manager.auth_api.authenticate(admin.creds)
    return admin

# Создаем движок (engine) для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{DBCreds.USERNAME}:{DBCreds.PASSWORD}"
    f"@{DBCreds.HOST}:{DBCreds.PORT}/{DBCreds.NAME}"
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

@pytest.fixture(scope="module")
def db_session():
    db_session = SessionLocal()
    yield db_session
    db_session.close()

@pytest.fixture()
def delay_between_retries():
    time.sleep(2)
    yield
