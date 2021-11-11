from enum import Enum

from test_data import TestData

import logging
import logging.config

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from PIL import Image
import os


class StatusTypes(Enum):
    """Enum for determining type of error in form"""
    complete = 0,
    error_data = 1,
    error_loading_time = 2


class Jet5Test:
    """Jet5 form Validator"""
    def __init__(self, test_data: TestData):
        # Instance of class TestData for read and generate test data
        self.test_data = test_data

        # Logger
        logging.config.fileConfig('logging.conf')
        self.__logger = logging.getLogger("jet5WebDriver")

        self.baseUrl = "https://jet5.ru/ru/"

        # Driver initialization
        self.s = Service('./drivers/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.s)

        self.__logger.info("Driver started")

    def _open_form(self):
        """Opening a web page and focusing on the form."""
        # Open website
        driver = self.driver
        driver.get(self.baseUrl)

        # Find form
        feedback_form = driver.find_element(By.ID, "form__feedback")

        # Scroll to form
        actions = ActionChains(driver)
        actions.move_to_element(feedback_form)
        actions.perform()

        return feedback_form

    def _send_data_to_form(self, form, is_negative=False):
        """Find all fields and enter data there """

        # Find every <input> field in form
        feedback_fields = form.find_elements(By.TAG_NAME, "input")

        # Find <textarea> because it's a separate tag unlike <input>
        textarea_message = form.find_element(By.NAME, "message")
        feedback_fields.append(textarea_message)

        for field in feedback_fields:
            attribute_name = field.get_attribute("name")
            if attribute_name in self.test_data.feedback_fields_dict:
                self.__logger.debug("InputName: " + attribute_name)
                field.send_keys(self.test_data.feedback_fields_dict[attribute_name])

        self.__logger.info("All data pasted...")

    def _get_feedback_status(self, form):
        """Get """
        delay = 3  # seconds
        status = ""

        try:
            feedback_message = WebDriverWait(form, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".feedback__message_show")))

            actions = ActionChains(self.driver)
            actions.move_to_element(feedback_message)
            actions.perform()

            feedback_classes = feedback_message.get_attribute("class")

            if "complete" in feedback_classes:
                status = StatusTypes.complete

            elif "error" in feedback_classes:
                status = StatusTypes.error_data

            return status
        except TimeoutException:
            return StatusTypes.error_loading_time
            # self.__logger.error("Loading took too much time!")

    def _press_send_btn(self, form):
        """Press on send form data button"""
        send_btn = form.find_element(By.CSS_SELECTOR, "button.feedback__button")
        send_btn.click()
        self.__logger.debug("Btn \"Send\" clicked")

    def validate(self):
        feedback_form = self._open_form()

        self._send_data_to_form(feedback_form)
        self._press_send_btn(feedback_form)
        feedback_status = self._get_feedback_status(feedback_form)

        if feedback_status == StatusTypes.complete:
            self.__logger.info("All data sent successfully")
        elif feedback_status == StatusTypes.error_data:
            self.__logger.error("Wrong data")
        elif feedback_status == StatusTypes.error_loading_time:
            self.__logger.error("Timeout error")
            self.element_screenshot(feedback_form)

        return feedback_status

    def element_screenshot(self, element):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        location = element.location_once_scrolled_into_view
        size = element.size
        self.driver.save_screenshot("./screenshots/pageImage.png")

        # crop image
        x = location['x']
        y = location['y']
        width = location['x'] + size['width']
        height = location['y'] + size['height']
        im = Image.open('./screenshots/pageImage.png')
        im = im.crop((int(x), int(y), int(width), int(height)))
        im.save('./screenshots/element.png')


# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     test_data = TestData()
#     print(test_data.set_negative())
#
#     jet5 = Jet5Test(test_data)
#     jet5.validate()
