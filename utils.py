import requests
from bs4 import BeautifulSoup


class Utils:
    @staticmethod
    def parse_html(text):
        tag_dict = {
            "<b>": "**",
            "</b>": "**",
            "<i>": "_",
            "</i>": "_"
        }
        new_text = text.replace('*', '\*')
        for i, j in tag_dict.items():
            new_text = new_text.replace(i, j)
        return new_text

    @staticmethod
    async def get_message() -> str:
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
                       + "\n**Przykład:**" + Utils.parse_html(example[0]) \
                       + "\n**URL**: " + redirected_url
        else:
            response = "**Słowo:** " + title[0] \
                       + "\n**Ocena:** " + rating \
                       + "\n**Definicja:** " + Utils.parse_html(definition[0]) \
                       + "\n**URL**: " + redirected_url
        return response

