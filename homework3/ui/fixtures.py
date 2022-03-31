import os
import shutil
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture
def driver(config):
    url = config['url']
    driver = get_driver()
    driver.get(url)
    yield driver
    driver.quit()


def get_driver():
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=opts)
    return driver


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)
