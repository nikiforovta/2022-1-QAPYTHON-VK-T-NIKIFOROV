import os.path
import uuid

import allure
from selenium.webdriver.support import expected_conditions as EC

from ui import locators
from ui.pages.base_page import BasePage


class CampaignPage(BasePage):
    locators = locators.CampaignPageLocators()

    @allure.step("Create campaign")
    def create_campaign(self):
        name = str(uuid.uuid4())
        self.click(self.locators.DIV_CLASS_LOCATOR('createButton'))
        self.click(self.locators.DIV_CLASS_LOCATOR('traffic'))
        self.send_keys(self.locators.URL_CHANGE_LOCATOR, self.driver.current_url)
        self.send_keys(self.locators.CAMPAIGN_NAME_CHANGE_LOCATOR, name, clear=True)
        self.click(self.locators.BANNER_LOCATOR)
        ele = self.wait().until(EC.presence_of_element_located(self.locators.UPLOAD_LOCATOR))
        ele.send_keys(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'photo.png'))
        self.click(self.locators.DIV_CLASS_LOCATOR('save-button'))
        return name
