import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
import allure

@allure.epic("UI tests")
@allure.feature("Login page test")
@pytest.mark.ui
class TestLogin:
    @allure.title("Successful login")
    def test_positive(self, registered_user, page: Page):
        login_page = LoginPage(page)

        login_page.open()
        login_page.login(email=registered_user.email, password=registered_user.password)

        login_page.assert_redirect_to_home_page()

        login_page.make_screenshot_and_attach_to_allure()

        login_page.assert_alert_popup()
