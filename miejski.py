import requests
from bs4 import BeautifulSoup

url = 'https://www.miejski.pl/losuj'

r = requests.get(url, allow_redirects=True)
http = BeautifulSoup(r.text, 'html.parser')
title = [x.get_text() for x in http.findAll("h1")]
definition = [x.get_text() for x in http.findAll("div", {"class": "definition summary"})]
example = [x.get_text() for x in http.findAll("div", {"class": "example"})]


print("\nSłowo: " + title[0])
print("\nDefinicja: " + definition[0])
print("==================================================", end="")
print(*example, sep="\n")
print("==================================================")
