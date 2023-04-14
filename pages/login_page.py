import allure


from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    # xpath кнопки принятия куки
    COOKIES_ACCEPT_BUTTON = (By.XPATH, "//button[text()='Allow all']")
    # xpath поля Email
    EMAIL_LOGIN_INPUT = (By.XPATH, "//input[@name='email']")
    # xpath поля Password
    PASSWORD_LOGIN_INPUT = (By.XPATH, "//input[@name='password']")
    # xpath кнопки Sign in
    SIGN_IN_BUTTON = (By.XPATH, "//span[text()='Sign in']")
    # xpath алерта при попытке логина с неправильными email и password
    INCORRECT_LOGIN_ALERT = (By.XPATH, "//span[@role='alert' and contains(text(), 'Incorrect email or password')]")
    # xpath алерта при попытке логина с невалидными email и password
    INVALID_LOGIN_ALERT = (By.XPATH, "//i[@class='e1je3lf i1v7rha4']")
    # xpath области инпутов логина и пароля
    LOGIN_FIELD = (By.XPATH, "//div[@class='rnhzm9g']")


class LoginPage(BasePage):
    email = "akorolenko13+ask_ev@gmail.com"  # в реальной жизни я бы это спрятал в энвах в гитлабе или брал из бд

    @allure.step("Принимаем куки")
    def accept_cookie(self):
        self.wait_and_click(*LoginPageLocators.COOKIES_ACCEPT_BUTTON)

    @allure.step("Логин в приложение: почта - {email}, пароль - {password} ")
    def login_user(self, email=email, password="tKuGiGVW7@8RHb7"):
        self.accept_cookie()
        self.clear_and_set_value(*LoginPageLocators.EMAIL_LOGIN_INPUT, email)
        password_field = self.browser.find_element(*LoginPageLocators.PASSWORD_LOGIN_INPUT)
        password_field.send_keys(password)
        self.wait_and_click(*LoginPageLocators.SIGN_IN_BUTTON)
