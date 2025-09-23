from playwright.sync_api import Page
from constants.constants import UI_BASE_URL, LOGIN_ENDPOINT, MOVIES
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{UI_BASE_URL}{LOGIN_ENDPOINT}"

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = "button[type='submit']"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # local actions
    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.click_element(self.login_button)

    def assert_redirect_to_home_page(self):
        self.wait_redirect_to_url(UI_BASE_URL)

    def assert_alert_popup(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")
