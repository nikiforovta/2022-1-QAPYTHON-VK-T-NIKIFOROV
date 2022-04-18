import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from ui import links


@pytest.fixture()
def open_my_target():
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="98.0.4758.102").install())
    driver.get(links.BASE_LINK)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
