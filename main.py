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

TEST_DATA = {
    "fio": ['Ivan'],
    "email": ["test@gmail.com"],
    "phone": ["81234567890"],
    "message": ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor."]
}


class Jet5Test:
    def __init__(self):
        # Logger
        logging.config.fileConfig('logging.conf')
        self.__logger = logging.getLogger("jet5")

        self.baseUrl = "https://jet5.ru/ru/"

        self.s = Service('./drivers/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.s)

        self.__logger.info("Driver started")

    def _open_form(self):
        driver = self.driver
        driver.get(self.baseUrl)
        feedback_form = driver.find_element(By.ID, "form__feedback")
        actions = ActionChains(driver)
        actions.move_to_element(feedback_form)
        actions.perform()

        return feedback_form

    def _send_data_to_form(self, form, is_negative=False):
        # Find every <input> field in form
        feedback_fields = form.find_elements(By.TAG_NAME, "input")

        for field in feedback_fields:
            attribute_name = field.get_attribute("name")
            if (attribute_name in TEST_DATA):
                self.__logger.debug("InputName: " + attribute_name)
                field.send_keys(TEST_DATA[attribute_name][1 if is_negative else 0])

        # Find <textarea> because it's a separate tag unlike <input>
        textarea_message = form.find_element(By.NAME, "message")
        textarea_message.send_keys(TEST_DATA["message"])

        self.__logger.info("All data pasted...")

    def _get_feedback_message(self, form):
        # feedback_message = form.find_element(By.CSS_SELECTOR, "feedback__message_show")
        delay = 5  # seconds

        try:
            feedback_message = WebDriverWait(form, delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".feedback__message_show")))

            actions = ActionChains(self.driver)
            actions.move_to_element(feedback_message)
            actions.perform()

            feedback_classes = feedback_message.get_attribute("class")

            if "complete" in feedback_classes:
                self.__logger.info("Send Formdata complete")

            elif "error" in feedback_classes:
                self.__logger.error("Send Formdata error")
        except TimeoutException:
            self.__logger.error("Loading took too much time!")

    def _press_send_btn(self, form):
        send_btn = form.find_element(By.CSS_SELECTOR, "button.feedback__button")
        send_btn.click()
        self.__logger.debug("Btn clicked")

    def validate(self):
        feedback_form = self._open_form()

        self._send_data_to_form(feedback_form)
        self._press_send_btn(feedback_form)
        feedback_message = self._get_feedback_message(feedback_form)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jet5 = Jet5Test()
    jet5.validate()
