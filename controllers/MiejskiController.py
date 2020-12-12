from typing import List

import requests
from asyncpg import Record
from bs4 import BeautifulSoup

from utils.Utils import Utils


class MiejskiMessage:

    def __init__(self, title: str, rating: str, definition: str, example=None):
        self.title = title
        self.rating = rating
        self.definition = definition
        self.example = example

    def has_example(self) -> bool:
        return self.example

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
        print(f"url: {r.request.url}")
        http = BeautifulSoup(r.text, 'html.parser')
        title = [x.get_text() for x in http.findAll("h1")][0].strip()
        definition = [x.get_text() for x in http.findAll("p")][0].strip()
        example = [x.get_text() for x in http.findAll("blockquote")]
        rating = http.find("span", {"class": "rating"}).contents[0]
        print(f"[Title: {title}, definition: {definition}, example: {example}, rating: {rating}]")
        return MiejskiMessage(title, rating, definition, example[0].strip()) if example else MiejskiMessage(
            title, rating, definition)

    @staticmethod
    def get_stats(records: List[Record]) -> str:
        result = "**STATYSTYKI**:\n"
        for i, record in enumerate(records):
            result += f'''**{i + 1}. {record['user_name']}**: {record['points']} pkt. \n'''
        return result
