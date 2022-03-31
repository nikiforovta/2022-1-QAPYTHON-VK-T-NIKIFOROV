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
    PROFILE_LOCATOR = (
        By.XPATH,
        "//div[starts-with(@class, 'right-module-rightWrap')]"
    )

    MENU_LOCATOR = lambda self, menu: (
        By.XPATH,
        f"//a[contains(@class, 'center-module-{menu}')]"
    )


class CampaignPageLocators(MainPageLocators):
    CAMPAIGN_LOCATOR = lambda self, name: (
        By.XPATH,
        f"//a[@title='{name}']"
    )

    DIV_CLASS_LOCATOR = lambda self, action: (
        By.XPATH,
        f"//div[contains(@class, '{action}')]"
    )

    URL_CHANGE_LOCATOR = (
        By.XPATH,
        "//input[contains(@class, 'mainUrl')]"
    )

    CAMPAIGN_NAME_CHANGE_LOCATOR = (
        By.XPATH,
        "//div[contains(@class, 'base-settings__campaign-name')]//input"
    )

    BANNER_LOCATOR = (
        By.XPATH,
        "//div[starts-with(@id, 'patterns_banner')]"
    )

    UPLOAD_LOCATOR = (
        By.XPATH,
        "//div[contains(@class, 'preview')]//input"
    )


class SegmentPageLocators(MainPageLocators):
    SEARCH_LOCATOR = (
        By.XPATH,
        "//input[contains(@class, 'search')]"
    )

    SEGMENT_LOCATOR = lambda self, name: (
        By.XPATH,
        f"//a[@title='{name}']"
    )

    ANDROID_SEGMENT_LOCATOR = (
        By.XPATH,
        "//div[text()[contains(., 'Android')]]"
    )

    CHECKBOX_CONTAINER = (
        By.XPATH,
        "//input[contains(@class, 'source-checkbox')]"
    )

    ADD_LOCATOR = (
        By.XPATH,
        "//div[contains(@class, 'add-button')]/button"
    )

    SEGMENT_NAME_CHANGE_LOCATOR = (
        By.XPATH,
        "//div[@class='js-segment-name']//input"
    )

    REMOVE_LOCATOR = lambda self, remove_id: (
        By.XPATH,
        f"//div[starts-with(@data-test, 'remove-{remove_id}')]/span"
    )

    BUTTON_LOCATOR = lambda self, action: (
        By.XPATH,
        f"//button[contains(@class, '{action}')]"
    )

    NO_RESULTS_LOCATOR = (
        By.XPATH,
        "//li[contains(@data-test, 'nothing')]"
    )
