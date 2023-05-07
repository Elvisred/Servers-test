import time
import allure
import pytest

from selenium.webdriver.common.by import By
from pages.contacts_page import ContactPage, ContactsPageLocators
from pages.login_page import LoginPage
from tests.conftest import random_string, random_number
from tests.base_test import BaseTest


@allure.epic("Contacts tests")
class TestContact(BaseTest):
    @pytest.fixture(autouse=True)
    def setup(self, browser):
        self.loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        self.contactpage = ContactPage(browser, BaseTest.baseurl)  # Инициализируем contactpage
        self.loginpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина
        self.loginpage.login_user()

    @allure.story("Contact create")
    @allure.title("Создание контакта")
    def test_correct_contact_create(self, browser):
        nickname = random_string(12)
        email = random_string(12) + "@test.com"

        self.contactpage.create_contact(nickname=nickname, email=email)

        with allure.step("Проверяем наличие области Contact info на /profile/contacts/{id}"):
            assert self.loginpage.is_element_present(*ContactsPageLocators.CONTACTS_FIELD)
        with allure.step(f"Проверка наличия никнейма {nickname}"):
            xpath_selector = f"//span[contains(text(),'{nickname}')]"
            assert self.contactpage.is_element_present(By.XPATH, xpath_selector), f"Никнейм {nickname} не найден"

    @allure.story("Contact delete")
    @allure.title("Удаление контакта")
    def test_correct_contact_delete(self, browser):
        phone_number = "+357" + random_number(8)

        self.contactpage.create_contact(phone_number=phone_number)
        self.loginpage.open(BaseTest.baseurl + "profile/contacts")  # Переходим на страницу списка контактов
        time.sleep(2)  # Вынужденный вейт
        self.contactpage.delete_contact_by_phone_number(phone_number)

        with allure.step(f"Проверяем отсутствие контакта с почтой {phone_number}"):
            xpath_selector = f"//td[normalize-space()='{phone_number}']"
            assert self.contactpage.is_not_element_present(By.XPATH, xpath_selector), f"телефон {phone_number} найден"
