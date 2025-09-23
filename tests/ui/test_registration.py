from pages.register_page import RegisterPage
from playwright.sync_api import Page
from utils.data_generator import DataGenerator
import allure
import pytest

@allure.epic("UI tests")
@allure.feature("Registration page test")
@pytest.mark.ui
class TestRegistration:
    @allure.title("Successful registration")
    def test_positive(self, page: Page):
        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = RegisterPage(page)

        register_page.open()
        register_page.register(full_name=f"PWTTest {random_name}", email=random_email,
                               password=random_password, confirm_password=random_password)

        register_page.assert_redirect_to_login_page()

        register_page.assert_alert_pop_up()
