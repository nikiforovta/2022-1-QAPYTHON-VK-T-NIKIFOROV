from appium.webdriver.common.mobileby import MobileBy


class BasePageLocators:
    TEXT_VIEW = lambda _, text: (MobileBy.XPATH, f'//android.widget.TextView[@text="{text}"]')


class MainPageLocators(BasePageLocators):
    KEYBOARD_INPUT = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    REQUEST_FIELD = (MobileBy.ID, 'ru.mail.search.electroscope:id/input_text')
    SEND_REQUEST_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/text_input_action')
    SETTINGS_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/assistant_menu_bottom')
    SUGGESTIONS = (MobileBy.ID, 'ru.mail.search.electroscope:id/suggests_list')
    POPULATION_REQUEST = BasePageLocators.TEXT_VIEW(BasePageLocators, "население россии")
    REPLY = (MobileBy.ID, 'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    PAUSE = (MobileBy.ID, 'ru.mail.search.electroscope:id/play_button')
    BACKWARD = (MobileBy.ID, 'ru.mail.search.electroscope:id/player_track_rev_button')
    TRACK = (MobileBy.ID, 'ru.mail.search.electroscope:id/player_track_name')


class AboutPageLocators(BasePageLocators):
    VERSION_INFO = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT_INFO = (MobileBy.ID, 'ru.mail.search.electroscope:id/about_copyright')


class SettingsPageLocators(BasePageLocators):
    SOURCE_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/user_settings_about')


class NewsSourceLocators(BasePageLocators):
    MAIL = BasePageLocators.TEXT_VIEW(BasePageLocators, "Новости Mail.ru")
