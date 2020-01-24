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
        # Attributes that the user (can) enter
        self.name = name
        self.artist = artist
        self.lyrics_query = lyrics_query

        self.full_name = ""  # This is for the name of the song with the artist and any features
        self.lyrics = ""  # This holds the original/full text representing the lyrics
        self.bare_lyrics = ""  # String of all of the words extracted without any new lines or punctuations

        # Stats about the song
        self.num_of_words = 0
        self.num_of_swear_words = 0
        self.num_of_lines = 0
        self.num_of_syllables = 0
        self.syllables_dict = {}  # Dictionary that holds the number of syllables of each word in the song

        # The grade level indices
        self.gunning_fog = 0
        self.flesch = 0
        self.power_sumner_kearl = 0

    # Besides the original three attributes that the user inputs, this method calculates all of the other stats and
    # indices
    def analyze(self):
        # If the user only entered a lyric query, just return the first hit
        if len(self.lyrics_query) > 0:
            # Gets the json response from Genius with the entered lyric query
            song_info = get_song_info(self.lyrics_query)
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
        self.num_of_lines = len(lines)
        for line in lines:
            if type(line) is None or len(line) == 0 or line[0] == "[":
                self.num_of_lines -= 1
                continue
            self.bare_lyrics += line + " "

        self.bare_lyrics = self.bare_lyrics.replace(",", "")
        self.bare_lyrics = self.bare_lyrics.replace("(", "")
        self.bare_lyrics = self.bare_lyrics.replace(")", "")
        self.bare_lyrics = self.bare_lyrics.lower()
        self.bare_lyrics = re.sub(r'[^a-zA-Z| ]', "", self.bare_lyrics)
        # print(self.bare_lyrics)
        bare_lyrics_split = self.bare_lyrics.split()
        self.num_of_words = len(bare_lyrics_split)
        Lyrics_set = set(bare_lyrics_split)

        num_of_big_words = 0

        for word in Lyrics_set:
            self.syllables_dict[word] = find_syllables(word)
                # greater than three syllables

        for word in bare_lyrics_split:
            if self.syllables_dict[word] >= 3:
                num_of_big_words += 1  # This is for the Gunning Fog index which needs the number of words that are
            self.num_of_syllables += self.syllables_dict[word]

        for word in self.swear_words:
            self.num_of_swear_words += self.bare_lyrics.count(word)

        # gunning fog index
        avg_sen_len = self.num_of_words / self.num_of_lines

        percentage_of_big_words = num_of_big_words / self.num_of_words
        # print(num_of_big_words)
        # print(self.num_of_words)
        self.gunning_fog = (avg_sen_len + percentage_of_big_words) * 0.4
        self.gunning_fog = float(f"{self.gunning_fog:.2f}")
        # print(avg_sen_len)
        # print(percentage_of_big_words)

        # The Flesch Formula
        x = self.num_of_words / self.num_of_lines * 1.015
        print(f"num of words is {self.num_of_words} and number lines is {self.num_of_lines} and x is {x}")
        y = self.num_of_syllables / self.num_of_words * 84.6
        print(f"{self.num_of_syllables} y is {y}")
        # print(self.num_of_syllabes)
        level = 206.835 - (x + y)

        if level <= 29:
            self.flesch = 'Very difficult Post Graduate'
        elif level <= 49:
            self.flesch = 'Difficult College'
        elif level <= 59:
            self.flesch = 'Fairly Difficult High School'
        elif level <= 69:
            self.flesch = 'Standard 8th to 9th grade'
        elif level <= 79:
            self.flesch = 'Fairly Easy 7th grade'
        elif level <= 89:
            self.flesch = 'Easy 5th to 6th grade'
        elif level <= 100:
            self.flesch = 'Very Easy 4th to 5th grade'
        else:
            self.flesch = 'Below 5th grade lmao'


        # Power Sumner Kearl
        x = self.num_of_words / self.num_of_lines
        # print("num of lines is: " + str(self.num_of_lines))
        y = self.num_of_syllables
        # print(f"x is{x} and y is {y}")
        y /= (self.num_of_words / 100)
        # print(f"x is{x} and y is {y}")
        z = (x * 0.0778) + (y * 0.0455)
        self.power_sumner_kearl = z - 2.2029
        self.power_sumner_kearl = float(f"{self.power_sumner_kearl:.2f}")