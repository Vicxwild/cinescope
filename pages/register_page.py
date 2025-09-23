from playwright.sync_api import Page
from constants.constants import UI_BASE_URL, REGISTER_ENDPOINT, MOVIES, LOGIN_ENDPOINT
from pages.page_action import PageAction

class RegisterPage(PageAction):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{UI_BASE_URL}{REGISTER_ENDPOINT}"

        # Element locators
        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"
        self.register_button = "button[type='submit']"
        self.sign_in_link = "a[href='/login' and text()='Войти']"

    # local actions
    def open(self):
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, password)

        self.click_element(self.register_button)

    def assert_redirect_to_login_page(self):
        self.wait_redirect_to_url(f"{UI_BASE_URL}login")

    def assert_alert_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")
