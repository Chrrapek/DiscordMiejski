import requests
from bs4 import BeautifulSoup
import discord
import os

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!miejski'):
        url = 'https://www.miejski.pl/losuj'

        r = requests.get(url, allow_redirects=True)
        http = BeautifulSoup(r.text, 'html.parser')
        redirected_url = http.find("link", {"rel": "canonical"})['href']
        title = [x.get_text() for x in http.findAll("h1")]
        definition = [x.get_text() for x in http.findAll("p")]
        example = [x.get_text() for x in http.findAll("blockquote")]

        if len(example) > 0:
            response = "**Słowo:** " + title[0] + "\n**Definicja:** " + definition[0] + "\n**Przykład:**" \
                       + example[0].replace('*', '\*') + "\n**URL**: " + redirected_url
        else:
            response = "**Słowo:** " + title[0] + "\n**Definicja:** " + definition[0] + "\n**URL**: " + redirected_url

        await message.channel.send(response)


client.run(os.environ.get('DISCORD_TOKEN'))
