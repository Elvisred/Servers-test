import allure
import pytest

from pages.login_page import LoginPage
from pages.profile_page import ProfilePage, ProfilePageLocators
from tests.base_test import BaseTest


@allure.epic("Profile tests")
class TestProfile(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        self.profilepage = ProfilePage(browser, BaseTest.baseurl)  # Инициализируем profilepage
        self.loginpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина
        self.loginpage.login_user()

    @pytest.mark.skip
    @allure.story("Account edit")
    @allure.title("Успешное редактирование аккаунта")
    def test_correct_edit_account(self, browser):
        """Тест отрабатывает корректно, но, как известно, после редактирования профиль нельзя
        редактировать на время проверки изменений и дальнейшие тесты невозможны. Добавлен для примера."""
        self.profilepage.edit_account()  # Редактируем аккаунт данными по умолчанию

        with allure.step("Проверяем наличие сообщения о проверке смены личных данных"):
            assert self.profilepage.is_element_present(*ProfilePageLocators.DATA_REQUEST_FIELD)

    @allure.story("Account edit cancel")
    @allure.title("Отмена редактирования аккаунта")
    def test_cancel_edit_account(self, browser):
        self.profilepage.edit_account(is_save=False)  # Редактируем аккаунт, но нажимаем на cancel

        with allure.step("Проверяем отсутствие сообщения о проверке смены личных данных"):
            assert self.profilepage.is_not_element_present(*ProfilePageLocators.DATA_REQUEST_FIELD)

    @pytest.mark.parametrize("empty_fields", [
        {"first_name": "", "last_name": ""},
        {"phone_number": "", "email": ""},
        {"city": "", "region": ""},
        {"postal_code": "", "street": ""}
    ])
    @allure.story("Account edit negative")
    @allure.title("Проверка обязательности полей при редактировании аккаунта")
    def test_empty_values_edit_account(self, browser, empty_fields):
        self.profilepage.edit_account(**empty_fields)

        with allure.step("Проверяем наличие аллертов о незаполненных обязательных полях"):
            assert self.profilepage.is_element_present(*ProfilePageLocators.EMPTY_FIELD_ALERT)
        with allure.step("Проверяем отсутствие сообщения о проверке смены личных данных"):
            assert self.profilepage.is_not_element_present(*ProfilePageLocators.DATA_REQUEST_FIELD)
