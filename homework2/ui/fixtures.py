import os
import shutil
import sys

import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.base_page import BasePage
from ui.pages.campaign_page import CampaignPage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.segment_page import SegmentPage


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)

    config.base_temp_dir = base_dir


@pytest.fixture
def driver(config):
    url = config['url']
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.get(url)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def campaign_page(driver):
    return CampaignPage(driver=driver)


@pytest.fixture
def segment_page(driver):
    return SegmentPage(driver=driver)
