import logging

import allure
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ui.locators import BasePageLocators

logger = logging.getLogger('test')


class BasePage(object):
    ACTION_RETRY = 3
    BASE_TIMEOUT = 5

    locators = BasePageLocators()

    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        logger.info(f'{self.__class__.__name__} page is opening...')

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @property
    def action_chains(self):
        return ActionChains(self.driver)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = self.BASE_TIMEOUT
        return WebDriverWait(self.driver, timeout=timeout)

    @allure.step('Кликаем на {locator}')
    def click_for_android(self, locator, timeout=None):
        for i in range(self.ACTION_RETRY):
            logger.info(f'Clicking on {locator}. Try {i + 1} of {self.ACTION_RETRY}...')
            try:
                element = self.find(locator, timeout=timeout)
                element.click()
                return
            except StaleElementReferenceException:
                if i == self.ACTION_RETRY - 1:
                    raise

    def swipe_up(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали вверх
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.2)
        end_y = int(dimension['height'] * 0.8)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_down(self, swipetime=200):
        """
        Базовый метод свайпа по вертикали вниз
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_right(self, swipetime=200):
        """
        Базовый метод свайпа по горизонтали вправо
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        start_x = int(dimension['width'] * 0.2)
        end_x = int(dimension['width'] * 0.8)
        y = int(dimension['height'] / 2)
        action. \
            press(x=start_x, y=y). \
            wait(ms=swipetime). \
            move_to(x=end_x, y=y). \
            release(). \
            perform()

    def swipe_left(self, swipetime=200):
        """
        Базовый метод свайпа по горизонтали влево
        Описание работы:
        1. узнаем размер окна телефона
        2. Задаем за X - центр нашего экрана
        3. Указываем координаты откуда и куда делать свайп
        4. TouchAction нажимает на указанные стартовые координаты, ждет и передвигает нас из одной точки в другую.
        5. release() наши пальцы с экрана, а perform() выполняет всю эту цепочку команд.
        """
        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        start_x = int(dimension['width'] * 0.8)
        end_x = int(dimension['width'] * 0.2)
        y = int(dimension['height'] / 2)
        action. \
            press(x=start_x, y=y). \
            wait(ms=swipetime). \
            move_to(x=end_x, y=y). \
            release(). \
            perform()

    def swipe_to_element(self, locator, max_swipes, direction):
        """
        :param locator: локатор, который мы ищем
        :param max_swipes: количество свайпов до момента, пока тест не перестанет свайпать в указанном направлении
        :param direction: направление свайпа
        """
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(f"Error with {locator}, please check function")
            if direction == 'up':
                self.swipe_up()
            elif direction == 'down':
                self.swipe_down()
            elif direction == 'left':
                self.swipe_left()
            else:
                self.swipe_right()
            already_swiped += 1

    def swipe_element_lo_left(self, locator):
        """
        :param locator: локатор, который мы ищем
        1. Находим наш элемент на экране
        2. Получаем его координаты (начала, конца по ширине и высоте)
        3. Находим центр элемента (по высоте)
        4. Делаем свайп влево, двигая центр элемента за его правую часть в левую сторону.
        """
        for i in range(self.ACTION_RETRY):
            logger.info(f'Swipe left on {locator}. Try {i + 1} of {self.ACTION_RETRY}...')
            try:
                element = self.find(locator, 10)
                right_x = element.rect['width'] * 0.55
                left_x = element.rect['width'] * 0.45
                upper_y = element.location['y']
                lower_y = upper_y + element.rect['height']
                y = (upper_y + lower_y) / 2
                action = TouchAction(self.driver)
                action. \
                    press(x=right_x, y=y). \
                    wait(ms=150). \
                    move_to(x=left_x, y=y). \
                    release(). \
                    perform()
                return
            except TimeoutException:
                if i == self.ACTION_RETRY - 1:
                    raise
