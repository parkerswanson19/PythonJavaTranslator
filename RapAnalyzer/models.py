import requests
import re
from django.db import models
# from .geniusGetter import *

from bs4 import BeautifulSoup


# Create your models here.
def find_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'lxml')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics


def get_song_info(*args):
    url = 'https://api.genius.com/search'
    headers = {'Authorization': 'Bearer ' + 'ULuimckPtpbjfzBpV-nOi0UtSfmcaHtuUmz5v1w8hWmgUQphXNvglKhbDk_yjTz8'}
    parameters = " ".join(args)
    data = {'q': parameters}
    # print("ARGS" + str(args))
    # print(type(*args))
    response = requests.get(url, headers=headers, data=data)
    # with open("kanye.json", "w") as file:
    #     file.write(str(response.json()))
    return response.json()


def find_syllables(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    diphthongs = ['ee', 'ea', 'oo', 'ie', 'ue', 'ay', 'au', 'ou', 'io', 'ei']
    triphthongs = ['eau', 'iou', 'ion', 'yea']

    counter = 0
    for vowel in vowels:
        counter += word.count(vowel)

    # print("number of vowels " + str(counter))

    i = 0
    while i < len(word):
        word_1 = word[i:i + 2]
        word_2 = word[i:i + 3]
        if word[i:i + 3] in triphthongs:
            counter -= 2
            i += 1
        elif word[i:i + 2] in diphthongs:
            counter -= 1

        i += 1

    if len(word) > 3:
        if word[-1] == 'e':
            counter -= 1
        elif word[-2:] == 'ed':
            counter -= 1

    # print(word + " has " + str(counter) + " syllables")
    return counter


class Song:
    swear_words = ["fuck", "motherfucker", "motherfuck", "shit", "bitch", "bitches", "nigga", "niggas", "ass",
                   "cunt", "cunts", "whore", "hoe", "slut", "bastard", "dick", "dicks", "pussy", "sluts", "dickhead",
                   "piss", "asshole", "damn", "goddamn"]

    drugs = ["percs", "percocet", "cocaine", "xan"]

    jewelery = ["patek"]

    def __init__(self, name, artist, lyrics_query):
        self.name = name
        self.full_name = ""
        self.artist = artist
        self.lyrics_query = lyrics_query
        self.lyrics = None
        self.bare_lyrics = ""
        self.num_of_words = 0
        self.num_of_swear_words = 0
        self.syllables = {}

    def analyze(self):
        if len(self.name) == 0 and len(self.artist) == 0:
            song_info = get_song_info(self.lyrics_query)
            # print(song_info["response"]["hits"])
            # print(type(song_info["response"]["hits"]))
            print(song_info["response"]["hits"][0]["result"]["url"])
            print(type(song_info["response"]["hits"]))
            self.lyrics = find_lyrics(song_info["response"]["hits"][0]["result"]["url"])
            self.full_name = song_info["response"]["hits"][0]["result"]["full_title"]


        else:
            song_info = get_song_info(self.name, self.artist)
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

                # print("User_input_name: " + user_input_name)
                # print("hit_name: " + hit_name)

                if user_input_name in hit_name:
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
        bare_lyrics_split = self.bare_lyrics.split()
        bare_lyrics_split = set(bare_lyrics_split)

        for word in bare_lyrics_split:
            self.syllables[word] = find_syllables(word)

        print(self.syllables)

        print("Num of unique words: " + str(len(self.syllables.keys())))
        self.num_of_words = len(bare_lyrics_split)

        for word in self.swear_words:
            self.num_of_swear_words += self.bare_lyrics.count(word)

