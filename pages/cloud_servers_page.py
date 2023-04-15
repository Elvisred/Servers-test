import allure

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPageLocators


class CloudServersPageLocators(object):
    # xpath чекбокса Yes, I want automatic backups
    BACKUP_ENABLE_CHECKBOX = (By.XPATH, "//input[@type='radio' and @name='backup_enabled' and @value='true']")
    # xpath инпута копий бэкапа
    BACKUP_INPUT = (By.XPATH, "//input[@name='backup_copies']")
    # xpath чекбокса No, I don't need automatic backups
    BACKUP_DISABLE_CHECKBOX = (By.XPATH, "//input[@type='radio' and @name='backup_enabled' and @value='false']")
    # xpath кнопки генерации SSH
    GENERATE_SSH_BUTTON = (By.XPATH, "//span[normalize-space()='Generate new SSH key']")
    # xpath инпута имени сервера
    SERVER_NAME_INPUT = (By.XPATH, "//input[@name='name']")
    # xpath кнопки Create cloud server
    CREATE_SERVER_BUTTON = (By.XPATH, "//button[@title='Create Cloud Server']")
    # xpath кнопки Cancel
    CANCEL_BUTTON = (By.XPATH, "//span[text()='Cancel']")

    # xpath элемента с текстом Payment methods
    PAYMENT_METHODS_TEXT = (By.XPATH, "//span[text()='Payment methods']")


class CloudServersPage(BasePage):
    def __init__(self, *args, **kwargs):
        super(CloudServersPage, self).__init__(*args, **kwargs)

    @allure.step("Вход на страницу создания облачного сервера")
    def enter_cloud_server_create(self):
        self.wait_and_click(*DashboardPageLocators.CLOUD_SERVERS_BUTTON)
        self.wait_and_click(*DashboardPageLocators.CLOUD_CREATE_BUTTON)
        self.wait_and_click(*DashboardPageLocators.CREATE_SERVER_BUTTON)

    @allure.step("Создание сервера")
    def create_server(
            self,
            country="Dallas",
            platform="Ubuntu 20.04-server (64 bit)",
            configuration="SSD.30",
            backup_enabled=True,
            backup_copies=None,
            server_name="test server",
            is_save=True
    ):
        self.enter_cloud_server_create()

        self.wait_and_click(By.XPATH, f"//span[contains(@class, 'li6amjs') and text()='{country}']")
        self.scroll_to_element(By.XPATH, f"//h4[text()='{platform}']/ancestor::label")
        self.wait_and_click(By.XPATH, f"//h4[text()='{platform}']/ancestor::label")
        self.scroll_to_element(By.XPATH, f"//h4[text()='{configuration}']/ancestor::label//input[@type='radio']")
        self.wait_and_click(By.XPATH, f"//h4[text()='{configuration}']/ancestor::label//input[@type='radio']")

        self.scroll_to_element(*CloudServersPageLocators.GENERATE_SSH_BUTTON)
        self.wait_and_click(*CloudServersPageLocators.GENERATE_SSH_BUTTON)

        if backup_enabled:
            self.scroll_to_element(*CloudServersPageLocators.BACKUP_ENABLE_CHECKBOX)
            self.wait_and_click(*CloudServersPageLocators.BACKUP_ENABLE_CHECKBOX)
            if backup_copies:
                self.clear_and_set_value(*CloudServersPageLocators.BACKUP_INPUT, backup_copies)
        else:
            self.wait_and_click(*CloudServersPageLocators.BACKUP_DISABLE_CHECKBOX)

        self.scroll_to_element(*CloudServersPageLocators.SERVER_NAME_INPUT)
        self.clear_and_set_value(*CloudServersPageLocators.SERVER_NAME_INPUT, server_name)

        if is_save:
            self.wait_and_click(*CloudServersPageLocators.CREATE_SERVER_BUTTON)
        else:
            self.wait_and_click(*CloudServersPageLocators.CANCEL_BUTTON)
