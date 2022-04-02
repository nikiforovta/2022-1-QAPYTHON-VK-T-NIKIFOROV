import os

import allure
import pytest
from appium import webdriver
from selenium.common.exceptions import TimeoutException

from ui.capability import capability_select
from ui.pages import BasePage, MainPage, SettingsPage, AboutPage, SourcePage


@pytest.fixture
def base_page(driver, config):
    return BasePage(driver=driver, config=config)


@pytest.fixture
def main_page(driver, config):
    return MainPage(driver=driver, config=config)


@allure.step("Разрешаем приложению доступ")
@pytest.fixture(scope='function')
def allow_all(base_page):
    try:
        while True:
            base_page.click_for_android(base_page.locators.ALLOW_BUTTON)
    except TimeoutException:
        pass


@pytest.fixture
def settings_page(driver, config):
    return SettingsPage(driver=driver, config=config)


@pytest.fixture
def about_page(driver, config):
    return AboutPage(driver=driver, config=config)


@pytest.fixture
def source_page(driver, config):
    return SourcePage(driver=driver, config=config)


def get_driver(appium_url):
    desired_caps = capability_select()
    driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
    return driver


@pytest.fixture(scope='function')
def app_version():
    files = os.listdir('../apk')
    return files[0].split('v')[-1].rsplit('.', 1)[0]


@pytest.fixture(scope='function')
def driver(config, test_dir):
    appium_url = config['appium']
    browser = get_driver(appium_url)
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir, config):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, 'failure.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'failure.png', attachment_type=allure.attachment_type.PNG)
