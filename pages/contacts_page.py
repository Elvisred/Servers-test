import allure

from enum import Enum
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from pages.dashboard_page import DashboardPageLocators
from tests.conftest import random_string, random_number
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class ContactsPageLocators(object):
    # xpath инпута first name
    FIRST_NAME_INPUT = (By.XPATH, "//input[@name='fname']")
    # xpath инпута middle name
    MIDDLE_NAME_INPUT = (By.XPATH, "//input[@name='tokens.middlename']")
    # xpath инпута last name
    LAST_NAME_INPUT = (By.XPATH, "//input[@name='lname']")
    # xpath инпута телефона
    PHONE_NUMBER_INPUT = (By.XPATH, "//input[@name='phone_number']")
    # xpath инпута email
    EMAIL_INPUT = (By.XPATH, "//input[@name='email']")
    # xpath инпута дополнительного email
    SECONDARY_EMAIL_INPUT = (By.XPATH, "//input[@name='email2']")
    # xpath области выбора job role
    JOB_ROLE_SELECTOR = (By.XPATH, "//div[@class='o1f4lk4c']")

    # xpath инпута Company
    COMPANY_INPUT = (By.XPATH, "//input[@name='tokens.company']")
    # xpath инпута Job title
    JOB_TITLE_INPUT = (By.XPATH, "//input[@name='tokens.title']")
    # xpath инпута Job role
    JOB_ROLE_INPUT = (By.XPATH, "//input[@name='tokens.role']")
    # xpath инпута Nickname
    NICKNAME_INPUT = (By.XPATH, "//input[@name='nickname']")
    # xpath инпута Comments
    COMMENTS_INPUT = (By.XPATH, "//textarea[@name='tokens.note']")
    # xpath кнопки Add more details
    CONTACT_DETAILS_BUTTON = (By.XPATH, "//span[normalize-space()='Add more details']")
    # xpath чекбокса Contact details
    CONTACT_DETAIL_SELECTOR = (By.XPATH, "//*[@class='select__control css-1s2u09g-control']")
    # xpath инпута Contact details
    CONTACT_INPUT = (By.XPATH, "//input[@name='contacts[0].value']")
    # xpath Create
    CREATE_BUTTON = (By.XPATH, "//span[normalize-space()='Create']")
    # xpath Cancel
    CANCEL_BUTTON = (By.XPATH, "//input[@name='phone_number']")

    # xpath области Contact info на странице /profile/contacts/{id}
    CONTACTS_FIELD = (By.XPATH, "//span[text()='Cancel']")
    # xpath подтверждения удаления контакта
    DELETE_CONTACT_ACCEPT = (By.XPATH, "//span[normalize-space()='Delete']")


class ContactPage(BasePage):

    class JobRole(Enum):
        PRIMARY = "Primary"
        TECHNICAL = "Technical"
        BILLING = "Billing"
        ABUSE = "Abuse"
        EMERGENCY = "Emergency"

    class ContactDetail(Enum):
        HOME_PHONE = "Home phone"
        WORK_PHONE = "Work phone"
        CELLPHONE = "Cell phone"
        FAX = "Fax"
        URL = "URL"

    def __init__(self, browser, url):
        super().__init__(browser, url)

    @allure.step("Вход на страницу создания контакта")
    def enter_create_contact(self):
        self.wait_and_click(*DashboardPageLocators.PROFILE_MENU_BUTTON)
        self.wait_and_click(*DashboardPageLocators.ENTER_CONTACTS)
        self.wait_and_click(*DashboardPageLocators.CREATE_CONTACT)

    @allure.step("Удаление контакта по номеру телефона")
    def delete_contact_by_phone_number(self, phone_number):
        self.wait_and_click(
            By.XPATH, f"//td[@class='tr1v0a t1qc42pv' and @data-label='Phone' and contains(text(), "
                      f"'{phone_number}')]/following-sibling::td/button"
        )
        self.wait_and_click(*ContactsPageLocators.DELETE_CONTACT_ACCEPT)
        self.wait_for_invisibility(By.XPATH, f"//td[contains(text(), '{phone_number}')]")

    @allure.step("Заполнение основных данных контакта")
    def fill_basic_data(self, first_name, middle_name, last_name, phone_number):
        self.scroll_to_element(*ContactsPageLocators.FIRST_NAME_INPUT)
        self.clear_and_set_value(*ContactsPageLocators.FIRST_NAME_INPUT, first_name)
        self.clear_and_set_value(*ContactsPageLocators.MIDDLE_NAME_INPUT, middle_name)
        self.clear_and_set_value(*ContactsPageLocators.LAST_NAME_INPUT, last_name)
        self.clear_and_set_value(*ContactsPageLocators.PHONE_NUMBER_INPUT, phone_number)

    @allure.step("Заполнение email данных контакта")
    def fill_email_data(self, email, secondary_email):
        self.clear_and_set_value(*ContactsPageLocators.EMAIL_INPUT, email)
        self.clear_and_set_value(*ContactsPageLocators.SECONDARY_EMAIL_INPUT, secondary_email)

    @allure.step("Заполнение рабочих данных контакта")
    def fill_work_data(self, company, job_title, job_role, nickname):
        self.clear_and_set_value(*ContactsPageLocators.COMPANY_INPUT, company)
        self.clear_and_set_value(*ContactsPageLocators.JOB_TITLE_INPUT, job_title)
        self.clear_and_set_value(*ContactsPageLocators.JOB_ROLE_INPUT, job_role)
        self.clear_and_set_value(*ContactsPageLocators.NICKNAME_INPUT, nickname)

    @allure.step("Заполнение комментария для контакта")
    def fill_comment_data(self, comments):
        self.clear_and_set_value(*ContactsPageLocators.COMMENTS_INPUT, comments)

    @allure.step("Выбор типа контакта")
    def select_job_role(self, job_role_type):
        self.scroll_to_element(*ContactsPageLocators.JOB_ROLE_SELECTOR)
        self.wait_and_click(By.XPATH, f"//label[contains(., '{job_role_type.value}')]/input[@type='checkbox']")

    '''Фантастически упрямые элементы селектора, я не смог их победить и жму в тесте "вручную".'''
    @allure.step("Выбор дополнительных контактов")
    def select_contact_detail(self, contact_detail: ContactDetail, contact_detail_input):
        self.wait_and_click(*ContactsPageLocators.CONTACT_DETAILS_BUTTON)
        self.wait_and_click(*ContactsPageLocators.CONTACT_DETAIL_SELECTOR)

        arrow_up_times = {
            self.ContactDetail.HOME_PHONE: 5,
            self.ContactDetail.WORK_PHONE: 4,
            self.ContactDetail.CELLPHONE: 3,
            self.ContactDetail.FAX: 2,
            self.ContactDetail.URL: 1
        }

        action = ActionChains(self.browser)
        for _ in range(arrow_up_times[contact_detail]):
            action.send_keys(Keys.ARROW_UP)
        action.send_keys(Keys.ENTER).perform()

        self.clear_and_set_value(*ContactsPageLocators.CONTACT_INPUT, contact_detail_input)

    @allure.step("Создание контакта")
    def create_contact(
            self,
            first_name=random_string(12),
            middle_name="",
            last_name=random_string(12),
            phone_number="+357" + random_number(8),
            email=random_string(12) + "@example.com",
            secondary_email="test2@example.com",
            company="Example Corp",
            job_title="QA",
            job_role="Development",
            nickname="Red Elvis",
            comments="Test contact",
            job_role_type=JobRole.BILLING,
            contact_detail=ContactDetail.FAX,
            contact_detail_input="+357" + random_number(8),
            is_save=True
    ):
        self.enter_create_contact()
        self.fill_basic_data(first_name, middle_name, last_name, phone_number)
        self.fill_email_data(email, secondary_email)
        self.select_job_role(job_role_type)
        self.fill_work_data(company, job_title, job_role, nickname)
        self.fill_comment_data(comments)
        self.select_contact_detail(contact_detail, contact_detail_input)

        if is_save:
            self.wait_and_click(*ContactsPageLocators.CREATE_BUTTON)
        else:
            self.wait_and_click(*ContactsPageLocators.CANCEL_BUTTON)
