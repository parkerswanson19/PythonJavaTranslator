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


def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'ULuimckPtpbjfzBpV-nOi0UtSfmcaHtuUmz5v1w8hWmgUQphXNvglKhbDk_yjTz8'}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response


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








song = request_song_info('sicko mode', 'travis scott')
json = song.json()
print(json)