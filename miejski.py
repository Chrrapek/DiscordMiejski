import requests 
import json
from bs4 import BeautifulSoup

url='https://www.miejski.pl/losuj'
#url='https://www.miejski.pl/slowo-elton'

r = requests.get(url, allow_redirects=True)
http = BeautifulSoup(r.text,'html.parser')
title = http.findAll("h1")
definition = http.findAll("div", {"class": "definition summary"})
example = http.findAll("div", {"class": "example"})


print("\nSłowo: "+title[0].string)
print("\nDefinicja: "+definition[0].string)
print("\n==================================================")
print(example[0].prettify().replace("<div class=\"example\">","").replace("</div>","").replace("<br/>",""))
print("==================================================")

