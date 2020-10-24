import requests
import json


class YesNoController:

    @staticmethod
    def get_response() -> str:
        url = "https://yesno.wtf/api"
        response = requests.get(url)
        return json.loads(response.text)["answer"]

