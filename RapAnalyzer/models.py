import requests
import re
from django.db import models
# from .geniusGetter import *

from bs4 import BeautifulSoup


# Create your models here.



def find_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

print(find_lyrics("https://genius.com/Travis-scott-sicko-mode-lyrics"))


def get_song_info(song_title, artist_name):
    url = 'https://api.genius.com/search'
    headers = {'Authorization': 'Bearer ' + 'ULuimckPtpbjfzBpV-nOi0UtSfmcaHtuUmz5v1w8hWmgUQphXNvglKhbDk_yjTz8'}
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(url, headers=headers, data=data)

    return response


class Song:
    swear_words = ["fuck", "motherfucker", "motherfuck", "shit", "bitch", "bitches", "nigga", "niggas", "ass",
                   "cunt", "cunts", "whore", "hoe", "slut", "bastard", "dick", "dicks", "pussy", "sluts", "dickhead",
                   "piss", "asshole", "damn", "goddamn"]

    drugs = ["percs", "percocet", "cocaine", "xan"]

    jewelery = ["patek"]

    def __init__(self, name, artist):
        self.name = name
        self.full_name = ""
        self.artist = artist
        self.lyrics = None
        self.bare_lyrics = ""
        self.num_of_words = 0
        self.num_of_swear_words = 0

    def analyze(self):
        song_info = get_song_info(self.name, self.artist)
        song_info = song_info.json()
        # with open("file.json", 'w') as file:
        #     file.write(str(song_info))

        for hit in song_info["response"]["hits"]:
            user_input_name = self.name.lower()
            user_input_name = user_input_name.replace(".", "")
            user_input_name = user_input_name.replace("(", "")
            user_input_name = user_input_name.replace(")", "")
            user_input_name = user_input_name.replace(",", "")

            hit_name = hit["result"]["title"].lower()
            hit_name = hit_name.replace(".", "")
            hit_name = hit_name.replace("(", "")
            hit_name = hit_name.replace(")", "")
            hit_name = hit_name.replace(",", "")
            hit_name = hit_name.replace(u'\u200b', "")

            if user_input_name == hit_name:
                self.lyrics = find_lyrics(hit["result"]["url"])
                self.full_name = hit["result"]["full_title"]
                break
        else:
            self.lyrics = "Error: Song not found. Check for typos."

        lines = self.lyrics.split("\n")
        for line in lines:
            if type(line) is None or len(line) == 0 or line[0] == "[":
                continue
            self.bare_lyrics += line + " "

        self.bare_lyrics = self.bare_lyrics.replace(",", "")
        self.bare_lyrics = self.bare_lyrics.replace("(", "")
        self.bare_lyrics = self.bare_lyrics.replace(")", "")
        self.bare_lyrics = self.bare_lyrics.lower()
        self.num_of_words = len(self.bare_lyrics.split())

        for word in self.swear_words:
            self.num_of_swear_words += self.bare_lyrics.count(word)

        print("YEET " + str (self.num_of_swear_words))
