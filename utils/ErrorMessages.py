import random


class ErrorMessages:

    @staticmethod
    def get_random_error_message() -> str:
        error_messages = [
            'Sorki, wykopyrtnąłem się i gdybym miał nóżki to bym nimi machał'
        ]
        return random.choice(error_messages)
