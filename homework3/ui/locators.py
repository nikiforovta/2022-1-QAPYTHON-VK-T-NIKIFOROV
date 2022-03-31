from selenium.webdriver.common.by import By


class LoginPageLocators:
    LOGIN_BUTTON_LOCATOR = (
        By.XPATH,
        '//div[starts-with(@class, "responseHead-module-button")]'
    )

    CREDENTIALS_INPUT_LOCATOR = lambda self, field: (
        By.CSS_SELECTOR,
        f'input[name="{field}"]'
    )

    LOGIN_LOCATOR = (
        By.XPATH,
        "//*[starts-with(@class, 'authForm-module-button')]"
    )

    ERROR_LOCATOR = (
        By.XPATH,
        "//div[contains(@class, 'error')]"
    )

    WRONG_DATA_LOCATOR = (
        By.XPATH,
        "//div[@class='formMsg_text']"
    )


class MainPageLocators:
    MENU_LOCATOR = lambda self, menu: (
        By.XPATH,
        f"//a[contains(@class, 'center-module-{menu}')]"
    )
