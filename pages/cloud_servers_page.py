import allure

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from pages.dashboard_page import DashboardPageLocators
from enum import Enum


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

    class Country(Enum):
        DALLAS = "Dallas"
        LUXEMBOURG = "Luxembourg"
        SINGAPORE = "Singapore"
        AMSTERDAM_AZ2 = "Amsterdam - az2"
        AMSTERDAM_AZ3 = "Amsterdam - az3"
        AMSTERDAM_AZ4 = "Amsterdam - az4"
        SAN_JOSE = "San Jose"
        WASHINGTON = "Washington"

    class Platform(Enum):
        CENTOS_7_64 = "CentOS 7 (64 bit)"
        DEBIAN_11_64 = "Debian 11 (64 bit)"
        ALMALINUX_8_64 = "AlmaLinux 8 (64 bit)"
        DEBIAN_10_64 = "Debian 10 (64 bit)"
        ROCKY_LINUX_8_64 = "Rocky Linux 8 (64 bit)"
        UBUNTU_18_04_SERVER_64 = "Ubuntu 18.04-server (64 bit)"
        UBUNTU_20_04_SERVER_64 = "Ubuntu 20.04-server (64 bit)"
        UBUNTU_22_04_SERVER_64 = "Ubuntu 22.04-server (64 bit)"

    class Configuration(Enum):
        SSD_30 = "SSD.30"
        SSD_50 = "SSD.50"
        SSD_80 = "SSD.80"
        SSD_100 = "SSD.100"
        SSD_120 = "SSD.120"
        SSD_180 = "SSD.180"
        SSD_320 = "SSD.320"
        SSD_480 = "SSD.480"
        SSD_640 = "SSD.640"

    @allure.step("Вход на страницу создания облачного сервера")
    def enter_cloud_server_create(self):
        self.wait_and_click(*DashboardPageLocators.CLOUD_SERVERS_BUTTON)
        self.wait_and_click(*DashboardPageLocators.CLOUD_CREATE_BUTTON)
        self.wait_and_click(*DashboardPageLocators.CREATE_SERVER_BUTTON)

    @allure.step("Выбор страны сервера")
    def select_server_country(self, country):
        self.wait_and_click(By.XPATH, f"//span[contains(@class, 'li6amjs') and text()='{country.value}']")

    @allure.step("Выбор платформы")
    def select_platform(self, platform):
        self.scroll_to_element(By.XPATH, f"//h4[text()='{platform.value}']/ancestor::label")
        self.wait_and_click(By.XPATH, f"//h4[text()='{platform.value}']/ancestor::label")

    @allure.step("Выбор конфигурации")
    def select_configuration(self, configuration):
        self.scroll_to_element(By.XPATH, f"//h4[text()='{configuration.value}']/ancestor::label//input[@type='radio']")
        self.wait_and_click(By.XPATH, f"//h4[text()='{configuration.value}']/ancestor::label//input[@type='radio']")

    @allure.step("Генерация SSH ключа")
    def generate_ssh_key(self):
        self.scroll_to_element(*CloudServersPageLocators.GENERATE_SSH_BUTTON)
        self.wait_and_click(*CloudServersPageLocators.GENERATE_SSH_BUTTON)

    @allure.step("Настройка автоматических резервных копий")
    def setup_backups(self, backup_enabled, backup_copies=None):
        if backup_enabled:
            self.scroll_to_element(*CloudServersPageLocators.BACKUP_ENABLE_CHECKBOX)
            self.wait_and_click(*CloudServersPageLocators.BACKUP_ENABLE_CHECKBOX)
            if backup_copies:
                self.clear_and_set_value(*CloudServersPageLocators.BACKUP_INPUT, backup_copies)
        else:
            self.wait_and_click(*CloudServersPageLocators.BACKUP_DISABLE_CHECKBOX)

    @allure.step("Установка имени сервера")
    def set_server_name(self, server_name):
        self.scroll_to_element(*CloudServersPageLocators.SERVER_NAME_INPUT)
        self.clear_and_set_value(*CloudServersPageLocators.SERVER_NAME_INPUT, server_name)

    @allure.step("Сохранение или отмена создания сервера")
    def save_or_cancel(self, is_save=True):
        if is_save:
            self.wait_and_click(*CloudServersPageLocators.CREATE_SERVER_BUTTON)
        else:
            self.wait_and_click(*CloudServersPageLocators.CANCEL_BUTTON)

    @allure.step("Создание сервера")
    def create_server(
            self,
            country=Country.DALLAS,
            platform=Platform.DEBIAN_11_64,
            configuration=Configuration.SSD_30,
            backup_enabled=True,
            backup_copies=None,
            server_name="test server",
            is_save=True
    ):
        self.enter_cloud_server_create()
        self.select_server_country(country)
        self.select_platform(platform)
        self.select_configuration(configuration)
        self.generate_ssh_key()
        self.setup_backups(backup_enabled, backup_copies)
        self.set_server_name(server_name)
        self.save_or_cancel(is_save)
