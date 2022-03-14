from selenium.webdriver.common.by import By

LOGIN_BUTTON_LOCATOR = (
    By.XPATH,
    '//*[starts-with(@class, "responseHead-module-button")]'
)

EMAIL_INPUT_LOCATOR = (
    By.CSS_SELECTOR,
    'input[name="email"]'
)

PASSWORD_INPUT_LOCATOR = (
    By.CSS_SELECTOR,
    'input[name="password"]'
)

LOGIN_LOCATOR = (
    By.XPATH,
    "//*[starts-with(@class, 'authForm-module-button')]"
)

MENU_LOCATOR = {
    'segments': (
        By.XPATH,
        "//a[contains(@class, 'center-module-segments')]"
    ),
    'billing': (
        By.XPATH,
        "//a[contains(@class, 'center-module-billing')]"
    )
}

CREATE_LOCATOR = (
    By.PARTIAL_LINK_TEXT,
    'Создайте'
)

COMMON_LOCATOR = (
    By.XPATH,
    "//div[3]/span"
)

PAYER_LOCATOR = (
    By.CSS_SELECTOR,
    "div.deposit__payment-form__subtitle"
)

AUTODEPOSIT_LOCATOR = (
    By.XPATH,
    "//li[@data-type='autodeposit']/span"
)

PROFILE_LOCATOR = (
    By.XPATH,
    "//*[starts-with(@class, 'right-module-rightWrap')]"
)

CAMPAIGN_LOCATOR = (
    By.PARTIAL_LINK_TEXT,
    'Создайте рекламную кампанию'
)

CHANGE_NAME_LOCATOR = (
    By.XPATH,
    "//div[@data-name='fio']/div/input"
)

SAVE_CHANGES = (
    By.CSS_SELECTOR,
    ".button"
)

SUCCESS_LOCATOR = (
    By.XPATH,
    "//div[contains(@data-class-name,'SuccessView')]/div[starts-with(@class, '_notification__content')]"
)

DROPDOWN_PROFILE_LOCATOR = (
    By.XPATH,
    "//ul[starts-with(@class, 'rightMenu-module-rightMenu')]"
)

LOGOUT_LOCATOR = (
    By.XPATH,
    "//ul[starts-with(@class, 'rightMenu-module-rightMenu')]/li[2]"
)

PROMOTE_LOCATOR = (
    By.XPATH,
    "//*[starts-with(@class, 'mainPage-module-bigTitle')]"
)

START_PROMOTION_LOCATOR = (
    By.XPATH,
    "//*[starts-with(@class, 'mainPage-module-description')]/div[2]"
)


def username_locator(name):
    return (
        By.CSS_SELECTOR,
        f'div[title="{name}"]'
    )
