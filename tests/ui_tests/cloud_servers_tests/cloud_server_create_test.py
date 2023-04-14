import allure

from pages.cloud_servers_page import CloudServersPage, CloudServersPageLocators
from pages.login_page import LoginPage
from tests.base_test import BaseTest


@allure.epic("Cloud servers tests")
class TestCloudServer(BaseTest):
    @allure.story("Cloud server")
    @allure.title("Проверка успешного создания облачного сервера")
    def test_correct_cloud_server(self, browser):
        # Arrange
        loginpage = LoginPage(browser, BaseTest.baseurl)  # Инициализируем loginpage
        cloudserverpage = CloudServersPage(browser, BaseTest.baseurl)  # Инициализируем cloudserverpage
        cloudserverpage.open(BaseTest.baseurl + "?login")  # Переходим на страницу логина
        loginpage.login_user()
        # Act
        cloudserverpage.create_server()  # создаем сервер с дефолтными значениями
        # Assert
        with allure.step("Проверяем переход на страницу выбора оплаты"):
            assert cloudserverpage.is_element_present(*CloudServersPageLocators.PAYMENT_METHODS_TEXT)
