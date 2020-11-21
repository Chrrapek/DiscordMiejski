import random


class ErrorMessages:

    @staticmethod
    def get_random_error_message() -> str:
        error_messages = [
            'Sorki, wykopyrtnąłem się i gdybym miał nóżki to bym nimi machał',
            'Coś... coś się popsuło i nie było nic słychać',
            'Coś nie pykło',
            'I cyk! A nie, jednak nie...'
        ]
        return random.choice(error_messages) + " :pepe_sad:"
