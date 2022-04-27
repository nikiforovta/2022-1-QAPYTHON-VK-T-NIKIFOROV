import uuid

from ui import locators
from ui.pages.base_page import BasePage


class SegmentPage(BasePage):
    locators = locators.SegmentPageLocators()

    def add_segment(self):
        name = str(uuid.uuid4())
        self.click(self.locators.BUTTON_LOCATOR('submit'))
        self.click(self.locators.ANDROID_SEGMENT_LOCATOR)
        self.click(self.locators.CHECKBOX_CONTAINER)
        self.click(self.locators.ADD_LOCATOR)
        self.send_keys(self.locators.SEGMENT_NAME_CHANGE_LOCATOR, name, clear=True)
        self.click(self.locators.BUTTON_LOCATOR('submit'))
        return name

    def remove_segment(self, name):
        to_remove = self.find(self.locators.SEGMENT_LOCATOR(name))
        remove_id = to_remove.get_attribute("href").split("/")[-1]
        loc = self.locators.REMOVE_LOCATOR(remove_id)
        self.click(loc)
        self.click(self.locators.BUTTON_LOCATOR('confirm'))
        return remove_id
