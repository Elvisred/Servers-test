import sys
import time

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC


class SeleniumWrapper:

    browser: WebDriver

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    # Глобальный тайм-аут и шаг проверки
    TIME_OUT = 60
    STEP = 0.1

    @allure.step("Нажимаем на элемент {what}")
    def wait_and_click(self, how, what, timeout=TIME_OUT, step=STEP):
        WebDriverWait(self.browser, timeout, step).until(EC.visibility_of_element_located((how, what)))
        self.browser.find_element(how, what).click()

    # Метод ожидания элемента
    def wait_for_visibility(self, how, what, timeout=TIME_OUT, step=STEP):
        WebDriverWait(self.browser, timeout, step).until(EC.visibility_of_element_located((how, what)))

    @allure.step("Ожидаем что элемент {what} отображен на странице")
    def is_visible(self, how, what, timeout=5, step=STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until(EC.visibility_of_element_located((how, what)))
        except TimeoutException:
            return False

        return True

    @allure.step("Ожидаем что элемент {what} присутствует на странице")
    def wait_for_presence(self, how, what, timeout=TIME_OUT, step=STEP):
        try:
            WebDriverWait(self.browser, timeout, step).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            raise AssertionError("Элемент отсутствует на странице")

    @allure.step("Проверяем что элемент {what} присутствует на странице")
    def is_element_present(self, how, what, timeout=TIME_OUT, step=STEP):
        """find element on the page"""
        try:
            WebDriverWait(self.browser, timeout, step).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    @allure.step("Скролл к элементу {what}")
    def scroll_to_element(self, how, what):
        self.wait_for_visibility(how, what)
        element = self.browser.find_element(how, what)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(3)

    @allure.step("Ожидаем что элемент отсутствует на странице")
    def is_not_element_present(self, how, what, timeout=5):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    @allure.step("Открываем страницу {url}")
    def open(self, url):
        """method to open the page"""
        self.browser.get(url)

    @allure.step("Очищаем значение и вводим {value} в текущем поле {what}")
    def clear_and_set_value(self, how, what, value=None):
        actions = ActionChains(self.browser)
        self.wait_and_click(how, what)
        element = self.browser.find_element(how, what)

        control_key = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL

        actions.move_to_element(element).click().key_down(control_key).send_keys("a").key_up(control_key).send_keys(
            Keys.DELETE).perform()

        if value:
            self.browser.find_element(how, what).send_keys(value)
