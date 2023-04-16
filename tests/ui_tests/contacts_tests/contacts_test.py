import time

import allure
from selenium.webdriver.common.by import By

from pages.contacts_page import ContactPage, ContactsPageLocators
from pages.login_page import LoginPage
from tests.conftest import random_string, random_number
from tests.base_test import BaseTest


@allure.epic("Contacts tests")
class TestContact(BaseTest):
    @allure.story("Contact create")
    @allure.title("Создание контакта")
    def test_correct_contact_create(self, browser):
        # Arrange
        loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        contactpage = ContactPage(browser, BaseTest.baseurl)  # Инициализируем contactpage
        loginpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина
        nickname = random_string(12)
        email = random_string(12) + "@test.com"
        loginpage.login_user()
        # Act
        contactpage.create_contact(nickname=nickname, email=email)
        # Assert
        with allure.step("Проверяем наличие области Contact info на /profile/contacts/{id}"):
            assert loginpage.is_element_present(*ContactsPageLocators.CONTACTS_FIELD)
        with allure.step(f"Проверка наличия никнейма {nickname}"):
            xpath_selector = f"//span[contains(text(),'{nickname}')]"
            assert contactpage.is_element_present(By.XPATH, xpath_selector), f"Никнейм {nickname} не найден"

    @allure.story("Contact delete")
    @allure.title("Удаление контакта")
    def test_correct_contact_delete(self, browser):
        # Arrange
        loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        contactpage = ContactPage(browser, BaseTest.baseurl)  # Инициализируем contactpage
        loginpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина
        phone_number = "+357" + random_number(8)
        loginpage.login_user()
        contactpage.create_contact(phone_number=phone_number)
        loginpage.open(BaseTest.baseurl + "profile/contacts")  # Переходим на страницу списка контактов
        time.sleep(2)
        # Act
        contactpage.delete_contact_by_phone_number(phone_number)
        # Assert
        with allure.step(f"Проверяем отсутствие контакта с почтой {phone_number}"):
            xpath_selector = f"//td[normalize-space()='{phone_number}']"
            assert contactpage.is_not_element_present(By.XPATH, xpath_selector), f"телефон {phone_number} найден"
