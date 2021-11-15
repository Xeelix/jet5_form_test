import random

FEEDBACK_FIELDS_ARRAY = ["fio", "email", "phone", "message"]


class TestData:
    def __init__(self):
        self.feedback_fields_dict = dict()

        self.set_by_data("")

    def set_by_data(self, data):
        for i, field in enumerate(FEEDBACK_FIELDS_ARRAY):
            # Singe data
            if not isinstance(data, list) or not isinstance(data, dict):
                self.feedback_fields_dict[field] = str(data)

            # Dict data
            if isinstance(data, dict):
                self.feedback_fields_dict[field] = data[field]

            # Array data
            if isinstance(data, list) and (len(data) == len(FEEDBACK_FIELDS_ARRAY)):
                self.feedback_fields_dict[field] = data[i]

        return self.feedback_fields_dict

    def set_by_params(self, fio=None, email=None, phone=None, message=None):
        if fio:
            self.feedback_fields_dict["fio"] = fio
        if email:
            self.feedback_fields_dict["email"] = email
        if phone:
            self.feedback_fields_dict["phone"] = phone
        if message:
            self.feedback_fields_dict["message"] = message

        return self.feedback_fields_dict

    def set_empty_fields(self):
        return self.set_by_data("")

    def set_positive(self):
        test = {
            "fio": "Test User",
            "email": "test@mail.ru",
            "phone": "79602328312",
            "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor."
        }

        return self.set_by_data(test)

    def set_negative(self, random_field=False):
        test = {
            "fio": "Test User",
            "email": "test@mail.ru",
            "phone": "79202312312",
            "message": "Lorem."
        }

        if random_field:
            i = random.randrange(0, len(FEEDBACK_FIELDS_ARRAY))
            test[FEEDBACK_FIELDS_ARRAY[i]] = ""
        else:
            test["email"] = "jtsd.com"

        return self.set_by_data(test)
