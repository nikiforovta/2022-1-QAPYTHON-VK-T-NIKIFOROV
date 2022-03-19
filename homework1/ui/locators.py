from selenium.webdriver.common.by import By

LOGIN_BUTTON_LOCATOR = (
    By.XPATH,
    '//div[starts-with(@class, "responseHead-module-button")]'
)

CREDENTIALS_INPUT_LOCATOR = lambda field: (
    By.CSS_SELECTOR,
    f'input[name="{field}"]'
)

LOGIN_LOCATOR = (
    By.XPATH,
    "//div[starts-with(@class, 'authForm-module-button')]"
)

MENU_LOCATOR = lambda menu: (
    By.XPATH,
    f"//a[contains(@class, 'center-module-{menu}')]"
)

CREATE_LOCATOR = (
    By.PARTIAL_LINK_TEXT,
    'Создайте'
)

PAYER_LOCATOR = (
    By.CSS_SELECTOR,
    "div.deposit__payment-form__subtitle"
)

PROFILE_LOCATOR = (
    By.XPATH,
    "//div[starts-with(@class, 'right-module-rightWrap')]"
)

CHANGE_NAME_LOCATOR = (
    By.XPATH,
    "//div[@data-name='fio']/div/input"
)

SAVE_CHANGES = (
    By.CSS_SELECTOR,
    ".button"
)

DROPDOWN_PROFILE_LOCATOR = (
    By.XPATH,
    "//ul[starts-with(@class, 'rightMenu-module-rightMenu')]"
)

LOGOUT_LOCATOR = (
    By.XPATH,
    "//a[@href='/logout']"
)

START_PROMOTION_LOCATOR = (
    By.XPATH,
    "//div[starts-with(@class, 'mainPage-module-description')]/div[2]"
)

USERNAME_LOCATOR = lambda name: (
    By.CSS_SELECTOR,
    f'div[title="{name}"]'
)
