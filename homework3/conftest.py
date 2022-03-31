import json
import logging

from api.client import TargetApiClient
from ui.fixtures import *
from ui.pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    debug_log = request.config.getoption('--debug_log')

    return {
        'url': url,
        'debug_log': debug_log
    }


@pytest.fixture(scope='function')
def logger(temp_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


@pytest.fixture(scope='session')
def credentials():
    with open('credentials.json') as credentials:
        credentials_json = json.load(credentials)
        user = credentials_json['EMAIL']
        password = credentials_json['PASSWORD']

    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config):
    driver = get_driver()
    driver.get(config['url'])
    login_page = LoginPage(driver)
    login_page.login(credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope="function")
def api_client(cookies) -> TargetApiClient:
    api_client = TargetApiClient(cookies)
    return api_client
