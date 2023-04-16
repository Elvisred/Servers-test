import allure

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class DashboardPageLocators(object):
    # xpath хедера страницы /dashboard
    DASHBOARD_HEADER = (By.XPATH, "//nav[@class='nn4rjii']")
    # xpath кнопки открытия селектора профиля/логаута
    PROFILE_AND_LOGOUT_BUTTON = (By.XPATH, "//div[@class='c1asuurm']/button")
    # xpath логаута
    LOGOUT_BUTTON = (By.XPATH, "//button/span[text()='Logout']")
    # xpath кнопки входа в профиль
    PROFILE_BUTTON = (By.XPATH, "//li/a/span[text()='Profile']")
    # xpath кнопки cloud servers
    CLOUD_SERVERS_BUTTON = (By.XPATH, "//span[text()='Cloud Servers']")
    # xpath кнопки create/manage в cloud servers
    CLOUD_CREATE_BUTTON = (By.XPATH, "//span[text()='Create & Manage']")
    # xpath кнопки create/manage в cloud servers
    CREATE_SERVER_BUTTON = (By.XPATH, "//span[text()='Create server']")
    # xpath кнопки Edit в профиле
    PROFILE_EDIT_BUTTON = (By.XPATH, "//span[text()='Edit']")
    # xpath кнопки Profile в правом меню
    PROFILE_MENU_BUTTON = (By.XPATH, "//span[contains(text(),'Profile')]")
    # xpath кнопки Contacts
    ENTER_CONTACTS = (By.XPATH, "//span[normalize-space()='Contacts']")
    # xpath кнопки на /profile/contacts
    CREATE_CONTACT = (By.XPATH, "//span[normalize-space()='Create']")
    # xpath кнопки удаления контакта
    DELETE_CONTACT = (By.XPATH, "//TODO")


class DashboardPage(BasePage):
    @allure.step("Logout пользователя")
    def logout_user(self):
        self.wait_and_click(*DashboardPageLocators.PROFILE_AND_LOGOUT_BUTTON)
        self.wait_and_click(*DashboardPageLocators.LOGOUT_BUTTON)
