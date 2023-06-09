import allure
import pytest

from pages.dashboard_page import DashboardPageLocators, DashboardPage
from pages.login_page import LoginPage, LoginPageLocators
from tests.conftest import random_string
from tests.base_test import BaseTest


@allure.epic("Login tests")
class TestLogin(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        self.loginpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина

    @allure.story("Login")
    @allure.title("Проверка успешного логина")
    def test_correct_login(self, browser):
        self.loginpage.login_user()

        with allure.step("Проверяем что перешли на /dachboard проверяя хедер этой страницы"):
            assert self.loginpage.is_element_present(*DashboardPageLocators.DASHBOARD_HEADER)

    @allure.story("Negative Login")
    @allure.title("Негативные тесты логина логина")
    @pytest.mark.parametrize(
        "case_index, email, password",
        [
            (0, f"not_exist_email_{random_string(5)}@gmail.com", random_string(12)),  # несуществующие логин и пароль
            (0, LoginPage.email, random_string(12)),  # реальный логин, неправильный пароль
            (1, f"no_password_{random_string(5)}@gmail.com", ""),  # валидный логин, пустой пароль
            (1, "", random_string(12)),  # пустой логин
            (1, f"short_password_{random_string(5)}@gmail.com", random_string(6)),  # короткий пароль
            (1, f"short_password_{random_string(5)}gmail.com", random_string(12)),  # невалидный логин
        ],
    )
    def test_negative_login(self, browser, case_index, email, password):
        self.loginpage.login_user(email=email, password=password)

        with allure.step("Проверяем сообщение об ошибке"):
            if case_index == 0:
                assert self.loginpage.is_element_present(*LoginPageLocators.INCORRECT_LOGIN_ALERT)
            elif case_index == 1:
                assert self.loginpage.is_element_present(*LoginPageLocators.INVALID_LOGIN_ALERT)

    @allure.story("Logout")
    @allure.title("Тест разлогина")
    def test_logout(self, browser):
        dashboardpage = DashboardPage(browser, BaseTest.baseurl)  # Инициализируем dashboardpage

        self.loginpage.login_user()
        dashboardpage.logout_user()
        # Assert
        with allure.step("Проверяем наличие поля логина и пароля при переходе на /login"):
            assert self.loginpage.is_element_present(*LoginPageLocators.LOGIN_FIELD)
