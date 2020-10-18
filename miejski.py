from typing import List

import requests
from asyncpg import Record
from bs4 import BeautifulSoup

from utils import Utils


class Miejski:
    @staticmethod
    async def get_message():
        url = 'https://www.miejski.pl/losuj'
        r = requests.get(url, allow_redirects=True)
        http = BeautifulSoup(r.text, 'html.parser')
        redirected_url = http.find("link", {"rel": "canonical"})['href']
        title = [x.get_text() for x in http.findAll("h1")]
        definition = [x.get_text() for x in http.findAll("p")]
        example = [x.get_text() for x in http.findAll("blockquote")]
        rating = http.find("span", {"class": "rating"}).contents[0]
        if len(example) > 0:
            response = "**Słowo:** " + title[0] \
                       + "\n**Ocena:** " + rating \
                       + "\n**Definicja:** " + Utils.parse_html(definition[0]) \
                       + "\n**Przykład:**" + Utils.parse_html(example[0])
        else:
            response = "**Słowo:** " + title[0] \
                       + "\n**Ocena:** " + rating \
                       + "\n**Definicja:** " + Utils.parse_html(definition[0])
        return rating, response

    @staticmethod
    def get_stats(records: List[Record]) -> str:
        result = "**STATYSTYKI**:\n"
        for i, record in enumerate(records):
            result += f'''**{i+1}. {record['user_name']}**: {record['points']} pkt. \n'''
        return result
