import requests
from django.db import models
# from .geniusGetter import *

from bs4 import BeautifulSoup


# Create your models here.
def find_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'lxml')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics


def get_song_info(song_title, artist_name):
    url = 'https://api.genius.com/search'
    headers = {'Authorization': 'Bearer ' + 'ULuimckPtpbjfzBpV-nOi0UtSfmcaHtuUmz5v1w8hWmgUQphXNvglKhbDk_yjTz8'}
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(url, headers=headers, data=data)

    return response


class Song:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.lyrics = None
        self.bare_lyrics = ""
        self.num_of_words = 0

    def analyze(self):
        song_info = get_song_info(self.name, self.artist)
        song_info = song_info.json()
        for hit in song_info["response"]["hits"]:
            if hit["result"]["title"].lower().replace(".", "") == self.name.lower().replace(".", ""):
                song = hit
                self.lyrics = find_lyrics(song["result"]["url"])
                break
        else:
            self.lyrics = "Error: Song not found. Check for typos."

        lines = self.lyrics.split("\n")
        for line in lines:
            if type(line) is None or len(line) == 0 or line[0] == "[":
                continue
            self.bare_lyrics += line + " "

        self.num_of_words = len(self.bare_lyrics.split())
        # print(self.lyrics)


