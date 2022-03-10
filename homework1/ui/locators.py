from selenium.webdriver.common.by import By

LOGIN_BUTTON_LOCATOR = (
    By.CSS_SELECTOR,
    '.responseHead-module-button-2yl51i'
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
    By.CSS_SELECTOR,
    ".authForm-module-button-1u2DYF"
)

MENU_LOCATOR = {
    'segments': (
        By.CSS_SELECTOR,
        'li.center-module-buttonWrap-1dlSMH:nth-child(2)'
    ),
    'billing': (
        By.CSS_SELECTOR,
        'li.center-module-buttonWrap-1dlSMH:nth-child(3)'
    )
}

CREATE_LOCATOR = (
    By.PARTIAL_LINK_TEXT,
    'Создайте'
)

COMMON_LOCATOR = (
    By.CSS_SELECTOR,
    "div.left-nav__group:nth-child(3) > span"
)

PAYER_LOCATOR = (
    By.CSS_SELECTOR,
    "div.deposit__payment-form__subtitle"
)

AUTODEPOSIT_LOCATOR = (
    By.CSS_SELECTOR,
    "li.page-tabs__tab-item:nth-child(2) > span"
)

PROFILE_LOCATOR = (
    By.CSS_SELECTOR,
    ".right-module-rightWrap-blvNjE"
)

CAMPAIGN_LOCATOR = (
    By.PARTIAL_LINK_TEXT,
    'Создайте рекламную кампанию'
)

CHANGE_NAME_LOCATOR = (
    By.CSS_SELECTOR,
    ".js-contacts-field-name > div > div > input"
)

SAVE_CHANGES = (
    By.CSS_SELECTOR,
    ".button"
)

SUCCESS_LOCATOR = (
    By.CSS_SELECTOR,
    "div._notification:nth-child(1) > div"
)

LOGOUT_LOCATOR = (
    By.CSS_SELECTOR,
    'li.rightMenu-module-rightMenuItem-1TjQzn:nth-child(2)'
)

DROPDOWN_PROFILE_LOCATOR = (
    By.CSS_SELECTOR,
    ".rightMenu-module-rightMenu-3VDfNR"
)

PROMOTE_LOCATOR = (
    By.CSS_SELECTOR,
    ".mainPage-module-bigTitle-3xPGEg"
)

START_PROMOTION_LOCATOR = (
    By.CSS_SELECTOR,
    ".mainPage-module-description-1k7oV8 > div:nth-child(3)"
)


def username_locator(name):
    return (
        By.CSS_SELECTOR,
        f'div[title="{name}"]'
    )
