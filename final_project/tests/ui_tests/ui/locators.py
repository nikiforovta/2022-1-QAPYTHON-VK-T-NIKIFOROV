from selenium.webdriver.common.by import By


class LoginPageLocators:
    CREDENTIALS_INPUT_LOCATOR = lambda self, name: (
        By.XPATH,
        f"//input[@id='{name}']"
    )

    REGISTRATION_LOCATOR = (
        By.XPATH,
        '//a[@href="/reg"]'
    )

    ERROR_LOCATOR = (
        By.XPATH,
        '//div[@id="flash"]'
    )


class RegistrationPageLocators:
    FORM_INPUT_LOCATOR = lambda self, name: (
        By.XPATH,
        f"//input[@id='{name}']"
    )

    LOGIN_LOCATOR = (
        By.XPATH,
        "//a[@href='/login']"
    )


class MainPageLocators:
    LOGOUT_LOCATOR = (
        By.XPATH,
        "//a[@href='/logout']"
    )

    HOME_LOCATOR = (
        By.XPATH,
        "//ul/a[@href='/']"
    )

    USERNAME_LOCATOR = (
        By.XPATH,
        '//div[@id="login-name"]//li[1]'
    )

    USER_LOCATOR = (
        By.XPATH,
        '//div[@id="login-name"]//li[2]'
    )

    VK_ID_LOCATOR = (
        By.XPATH,
        '//div[@id="login-name"]//li[3]'
    )

    RANDOM_FACT_LOCATOR = (
        By.XPATH,
        '//div/p[1]'
    )

    CENTER_CONTENT_LOCATOR = lambda self, i: (
        By.XPATH,
        f'(//div[starts-with(@class, "uk-grid")]//a)[{i}]'
    )

    NAVBAR_LOCATOR = lambda self, i: (
        By.XPATH,
        f'//ul[@class="uk-navbar-nav uk-hidden-small"]/li[{i}]'
    )

    NAVBAR_SUB_LOCATOR = lambda self, i, j: (
        By.XPATH,
        f'(//ul[@class="uk-navbar-nav uk-hidden-small"]/li[{i}]//a)[{j}]'
    )
