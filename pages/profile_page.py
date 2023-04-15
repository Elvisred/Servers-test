import allure

from enum import Enum
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPageLocators
from tests.conftest import random_string, random_number


class ProfilePageLocators(object):
    # xpath чекбокса personal
    PERSONAL_CHECKBOX = (By.XPATH, "//input[@name='business_type' and @value='0']")
    # xpath чекбокса business
    BUSINESS_CHECKBOX = (By.XPATH, "//input[@name='business_type' and @value='1']")
    # xpath элемента с текстом об обработке о смене персональных данных
    DATA_REQUEST_FIELD = (By.XPATH, "//span[contains(text(),'Your personal data changing request is in process.')]")

    # xpath чекбокса выбора доллара
    CURRENCY_DOLLAR_CHECKBOX = (By.XPATH, "//input[@name='currency' and @value='USD']")
    # xpath чекбокса выбора евро
    CURRENCY_EURO_CHECKBOX = (By.XPATH, "//input[@name='currency' and @value='EUR']")

    # xpath маркетинговой рассылки
    MARKETING_EMAIL_CHECKBOX = (By.XPATH, "//input[@name='newsletters_subscription']")

    # xpath инпутаfirst name
    FIRST_NAME_INPUT = (By.XPATH, "//input[@name='fname']")
    # xpath инпута last name
    LAST_NAME_INPUT = (By.XPATH, "//input[@name='lname']")
    # xpath инпута телефона
    PHONE_NUMBER_INPUT = (By.XPATH, "//input[@name='phone_number']")
    # xpath инпута email
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")

    # xpath селектора страны
    COUNTRY_SELECTOR = (By.XPATH, "//div[@class='select__input-container css-ackcql']")
    # xpath селектора города
    CITY_SELECTOR = (By.XPATH, "//input[@name='billing_address_city']")
    # xpath инпута региона
    REGION_INPUT = (By.XPATH, "//input[@name='billing_address_region']")
    # xpath инпута индекса
    POSTAL_CODE_INPUT = (By.XPATH, "//input[@name='billing_address_postalcode']")
    # xpath инпута города
    STREET_INPUT = (By.XPATH, "//input[@name='billing_address_street']")

    # xpath кнопки save
    SAVE_BUTTON = (By.XPATH, "//button[@title='Save']")
    # xpath кнопки cancel
    CANCEL_BUTTON = (By.XPATH, "//span[normalize-space()='Cancel']")

    # xpath алерта о незаполненном обязательном поле
    EMPTY_FIELD_ALERT = (By.XPATH, "//i[@class='e1j9utep idfhz4m']")


class ProfilePage(BasePage):
    def __init__(self, *args, **kwargs):
        super(ProfilePage, self).__init__(*args, **kwargs)

    """Сюда также можно вбить остальные валюты и расширить метод по выбору валюты"""
    class Currency(Enum):
        USD = "USD"
        EUR = "EUR"

    class BusinessType(Enum):
        PERSONAL = "personal"
        BUSINESS = "business"

    @allure.step("Вход на страницу редактирования профиля")
    def enter_edit_account(self):
        self.wait_and_click(*DashboardPageLocators.PROFILE_AND_LOGOUT_BUTTON)
        self.wait_and_click(*DashboardPageLocators.PROFILE_BUTTON)
        self.wait_and_click(*DashboardPageLocators.PROFILE_EDIT_BUTTON)

    @allure.step("Выбор типа бизнеса")
    def select_business_type(self, business_type):
        if business_type == self.BusinessType.PERSONAL:
            self.wait_and_click(*ProfilePageLocators.PERSONAL_CHECKBOX)
        elif business_type == self.BusinessType.BUSINESS:
            self.wait_and_click(*ProfilePageLocators.BUSINESS_CHECKBOX)

    @allure.step("Выбор валюты")
    def select_currency(self, currency):
        if currency == self.Currency.USD:
            self.wait_and_click(*ProfilePageLocators.CURRENCY_DOLLAR_CHECKBOX)
        elif currency == self.Currency.EUR:
            self.wait_and_click(*ProfilePageLocators.CURRENCY_EURO_CHECKBOX)

    @allure.step("Установка настроек маркетинговой рассылки")
    def set_marketing_email(self, marketing_email):
        if marketing_email is True:
            self.wait_and_click(*ProfilePageLocators.MARKETING_EMAIL_CHECKBOX)

    @allure.step("Заполнение данных пользователя")
    def fill_user_data(self, first_name, last_name, phone_number, email):
        self.scroll_to_element(*ProfilePageLocators.FIRST_NAME_INPUT)
        self.clear_and_set_value(*ProfilePageLocators.FIRST_NAME_INPUT, first_name)
        self.clear_and_set_value(*ProfilePageLocators.LAST_NAME_INPUT, last_name)
        self.clear_and_set_value(*ProfilePageLocators.PHONE_NUMBER_INPUT, phone_number)
        self.clear_and_set_value(*ProfilePageLocators.EMAIL_INPUT, email)

    @allure.step("Заполнение адресных данных")
    def fill_address_data(self, country, city, region, postal_code, street):
        self.wait_and_click(*ProfilePageLocators.COUNTRY_SELECTOR)
        self.wait_and_click(By.XPATH, f"//div[contains(text(),{country})]")
        self.clear_and_set_value(*ProfilePageLocators.CITY_SELECTOR, city)
        self.clear_and_set_value(*ProfilePageLocators.REGION_INPUT, region)
        self.clear_and_set_value(*ProfilePageLocators.POSTAL_CODE_INPUT, postal_code)
        self.clear_and_set_value(*ProfilePageLocators.STREET_INPUT, street)

    @allure.step("Сохранение или отмена редактирования аккаунта")
    def save_or_cancel_edit(self, is_save=True):
        if is_save is True:
            self.wait_and_click(*ProfilePageLocators.SAVE_BUTTON)
        else:
            self.wait_and_click(*ProfilePageLocators.CANCEL_BUTTON)

    @allure.step("Редактирование аккаунта")
    def edit_account(
            self,
            first_name="Aleksei",
            last_name="Korolenko",
            phone_number="+3570000000",
            email=f"{random_string(16)}@test.com",
            country="Cyprus",
            city="Larnaca",
            region="Cyprus",
            postal_code=random_number(4),
            street="Ermou 31",
            currency=Currency.USD,
            business_type=BusinessType.PERSONAL,
            marketing_email=True,
            is_save=True
    ):
        self.select_business_type(business_type)
        self.select_currency(currency)
        self.set_marketing_email(marketing_email)
        self.fill_user_data(first_name, last_name, phone_number, email)
        self.fill_address_data(country, city, region, postal_code, street)
        self.save_or_cancel_edit(is_save)
