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


class Song:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist
        self.lyrics = ""

    def analyze(self):
        # try:
        name = self.name.split()
        name = "-".join(name).replace(".", "")
        artist = self.artist.split()
        artist = "-".join(artist).replace(".", "")

        url = f"https://genius.com/{artist}-{name}-lyrics"
        self.lyrics = find_lyrics(url)
