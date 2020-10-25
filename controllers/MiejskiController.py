from typing import List

import requests
from asyncpg import Record
from bs4 import BeautifulSoup

from utils.Utils import Utils


class MiejskiMessage:

    def __init__(self, title: str, rating: str, definition: str, example: str):
        self.title = title
        self.rating = rating
        self.definition = definition
        self.example = example

    def has_example(self) -> bool:
        return len(self.example) > 0

    def to_string(self) -> str:
        if self.has_example():
            return self.to_string_without_example() + self.example_to_string()
        else:
            return self.to_string_without_example()

    def to_string_without_example(self):
        return "**Słowo:** " + self.title \
               + "\n**Ocena:** " + self.rating \
               + "\n**Definicja:** " + Utils.parse_html(self.definition)

    def example_to_string(self) -> str:
        return "\n**Przykład:** " + Utils.parse_html(self.example)


class Miejski:
    @staticmethod
    async def get_message() -> MiejskiMessage:
        url = 'https://www.miejski.pl/losuj'
        r = requests.get(url, allow_redirects=True)
        http = BeautifulSoup(r.text, 'html.parser')
        title = [x.get_text() for x in http.findAll("h1")]
        definition = [x.get_text() for x in http.findAll("p")]
        example = [x.get_text() for x in http.findAll("blockquote")]
        rating = http.find("span", {"class": "rating"}).contents[0]
        print(f"title: {title}\ndefinition: {definition}\nexample: {example}\nrating: {rating}")
        return MiejskiMessage(title[0], rating[0], definition[0], example[0])

    @staticmethod
    def get_stats(records: List[Record]) -> str:
        result = "**STATYSTYKI**:\n"
        for i, record in enumerate(records):
            result += f'''**{i + 1}. {record['user_name']}**: {record['points']} pkt. \n'''
        return result
