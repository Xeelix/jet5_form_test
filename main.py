from selenium import webdriver
from selenium import webdriver
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
        self.baseUrl = "https://jet5.ru/ru/"

        self.s = Service('./drivers/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.s)

        self._send_data_to_form(self._open_form())

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
                print(attribute_name)
                field.send_keys(TEST_DATA[attribute_name][1 if is_negative else 0])

        # Find <textarea> because it's a separate tag unlike <input>
        textarea_message = form.find_element(By.NAME, "message")
        textarea_message.send_keys(TEST_DATA["message"])

        print("All data pasted...")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    jet5 = Jet5Test()
