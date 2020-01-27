import requests
import re
from django.db import models
from bs4 import BeautifulSoup


def to_database(title_, lyrics_, swear_words, num_words, artist_, url_, jewelry_, drugs_, g, f, p,
                adlibs_, lines_, syllables_, big, sentences_):
    obj = SongDB(title=title_, lyrics=lyrics_, num_of_words=num_words, url=url_,
                 num_of_swear_words=swear_words, artist=artist_, jewelry=jewelry_,
                 drugs=drugs_, reading_level_g=g, reading_level_f=f, reading_level_p=p,
                 adlibs=adlibs_, lines=lines_, syllables=syllables_, big_words=big,
                 sentence_length=sentences_)
    obj.save()


def find_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    lyrics = soup.find('div', class_='lyrics').get_text()
    return lyrics


def get_song_info(*args):
    url = 'https://api.genius.com/search'
    headers = {'Authorization': 'Bearer ' + 'ULuimckPtpbjfzBpV-nOi0UtSfmcaHtuUmz5v1w8hWmgUQphXNvglKhbDk_yjTz8'}
    parameters = " ".join(args)
    data = {'q': parameters}
    response = requests.get(url, headers=headers, data=data)
    # with open("test.json", "w") as file:
    #     file.write(str(response.json()))
    return response.json()


def find_syllables(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    diphthongs = ['ee', 'ea', 'oo', 'ie', 'ue', 'ay', 'au', 'ou', 'io', 'ei']
    triphthongs = ['eau', 'iou', 'ion', 'yea']

    counter = 0
    for vowel in vowels:
        counter += word.count(vowel)

    i = 0
    while i < len(word):
        # word_1 = word[i:i + 2]
        # word_2 = word[i:i + 3]
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

    return counter


class SongDB(models.Model):
    num_of_words = models.IntegerField()
    title = models.TextField()
    artist = models.TextField()
    lyrics = models.TextField()
    num_of_swear_words = models.IntegerField()
    url = models.URLField()
    jewelry = models.IntegerField()
    drugs = models.IntegerField()
    reading_level_g = models.FloatField()
    reading_level_f = models.TextField()
    reading_level_p = models.FloatField()
    adlibs = models.IntegerField()
    lines = models.IntegerField()
    syllables = models.IntegerField()
    big_words = models.IntegerField()
    sentence_length = models.IntegerField()

    def __str__(self):
        return self.title


class Song:
    swear_words = ["fuck", "fucker", "motherfucker", "motherfuck", "shit", "bitch", "bitches", "nigga", "niggas", "ass",
                   "cunt", "cunts", "whore", "hoe", "slut", "bastard", "dick", "dicks", "pussy", "sluts", "dickhead",
                   "piss", "asshole", "damn", "goddamn", "titty", "titties", ]

    drugs = ["percs", "percocet", "cocaine", "xan", "molly", "weed", "drugs", "coke", "lean", "8th", "dirty sprite",
             "codeine", "blunt", "xannie", "acid", "shrooms", "blow", "crack", "powder", "coca", "heroin",
             "420", "broccoli", "cush", "mary jane", "meth", "Act", "addies", "addy"]

    jewelery = ["patek", "rollie", "chain", "phillipe", "rolex", "diamond", "richard", "millie", "audemars", "piguet"
                , "cuban", "cartier", "ice", "icy", ]

    def __init__(self, song_title, artist, lyrics_query):
        # Attributes that the user (can) enter
        self.song_title = song_title
        self.artist = artist
        self.lyrics_query = lyrics_query

        self.full_name = ""  # This is for the name of the song with the artist and any features
        self.lyrics = ""  # This holds the original/full text representing the lyrics, meant to be displayed to user
        self.bare_lyrics = ""  # String of all of the words extracted without any new lines, punctuations, or headers
        # ^ Meant to be used in analysis
        self.url = ""

        # Stats about the song
        self.num_of_words = 0
        self.num_of_swear_words = 0
        self.num_of_drug_references = 0
        self.num_of_jewelery_references = 0
        self.num_of_adlibs = 0

        # The grade level indices
        self.gunning_fog = 0
        self.flesch = 0
        self.power_sumner_kearl = 0

        # Parameters needs by the indices
        self.num_of_lines = 0
        self.num_of_syllables = 0
        self.syllables_dict = {}  # Dictionary that holds the number of syllables of each word in the song
        self.num_of_big_words = 0  # The number of words with three or more syllables, used by the indices
        self.avg_sen_len = 0  # The average sentence length

    # Besides the original three attributes that the user inputs, this method calculates all of the other stats and
    # indices
    def analyze(self):
        ####################################################
        # First, the song lyrics and the full name are found
        ####################################################

        # If the user entered a lyric query, just return the first hit
        if len(self.lyrics_query) > 0:
            # Gets the json response from Genius with the entered lyric query
            song_info = get_song_info(self.lyrics_query, self.artist)
            if len(song_info["response"]["hits"]) < 1:  # If not hits are there, then return
                self.lyrics = "Error: Song not found. Check for typos."
                return
            # Gets the lyrics by passing in the url of the first search result to find_lyrics()
            self.lyrics = find_lyrics(song_info["response"]["hits"][0]["result"]["url"])
            # ALso gets the song's full name
            self.full_name = song_info["response"]["hits"][0]["result"]["full_title"]
        else:
            song_info = get_song_info(self.song_title, self.artist)
            # with open("file.json", 'w') as file:
            #     file.write(str(song_info))

            for hit in song_info["response"]["hits"]:
                user_input_name = self.song_title.lower()  # Make the title lowercase for consistency

                # Remove all extra characters to make comparison easier for user
                user_input_name = re.sub('.|\(|\)|,', '', user_input_name)

                hit_name = hit["result"]["title"].lower()  # Make lowercase
                # Remove all extra characters to make comparison easier for user
                hit_name = re.sub('.|\(|\)|,|\u200b', '', hit_name)

                # user_input_name = user_input_name.replace(".", "")
                # user_input_name = user_input_name.replace("(", "")
                # user_input_name = user_input_name.replace(")", "")
                # user_input_name = user_input_name.replace(",", "")
                # hit_name = hit_name.replace(".", "")
                # hit_name = hit_name.replace("(", "")
                # hit_name = hit_name.replace(")", "")
                # hit_name = hit_name.replace(",", "")
                # hit_name = hit_name.replace(u'\u200b', "")
                # print("User_input_name: " + user_input_name)
                # print("hit_name: " + hit_name)

                if user_input_name in hit_name:
                    self.lyrics = find_lyrics(hit["result"]["url"])
                    self.full_name = hit["result"]["full_title"]
                    break
            else:
                self.lyrics = "Error: Song not found. Check for typos."
                return

        #########################################################################
        # Second, the number of lines, words, and syllables of each word is found
        #########################################################################

        lines = self.lyrics.split("\n")
        self.num_of_lines = len(lines)
        for line in lines:
            if type(line) is None or len(line) == 0 or line[0] == "[":
                self.num_of_lines -= 1
                continue
            # Only adds lines that are actual lyrics of the song, not headers
            self.bare_lyrics += line + " "

        # Removes all non alphanumeric characters from the lyrics
        self.bare_lyrics = re.sub(r'[^a-zA-Z| |0-9]', "", self.bare_lyrics)
        # print(self.bare_lyrics)
        # self.bare_lyrics = re.sub(",|\(|\)", '', self.bare_lyrics)
        # self.bare_lyrics = self.bare_lyrics.replace(",", "")
        # self.bare_lyrics = self.bare_lyrics.replace("(", "")
        # self.bare_lyrics = self.bare_lyrics.replace(")", "")
        self.bare_lyrics = self.bare_lyrics.lower()

        # print(self.bare_lyrics)
        # Makes a list of each individual word
        bare_lyrics_split = self.bare_lyrics.split()
        self.num_of_words = len(bare_lyrics_split)  # Counts the number of words in the song

        #######################################################################################################
        # Third, the number of syllables for each word, the total number of syllables, and the average sentence
        # length are calculated, essentially all of the stats needed by the formulas
        #######################################################################################################

        # Creates a set where each lyric only appears once, used to speed up syllable calculations
        lyrics_set = set(bare_lyrics_split)

        # Goes through each word and finds the number of syllables
        for word in lyrics_set:
            self.syllables_dict[word] = find_syllables(word)
            # greater than three syllables

        for word in bare_lyrics_split:
            if self.syllables_dict[word] >= 3:
                self.num_of_big_words += 1  # This is for the Gunning Fog index which needs the number of words that are
            self.num_of_syllables += self.syllables_dict[word]

        ###########################################################
        # Fourth, the three grade level measurements are calculated
        ###########################################################
        # https://www.tameri.com/teaching/levels.html

        # Gunning Fog index
        self.avg_sen_len = self.num_of_words / self.num_of_lines  # Finds the average sentence length
        percentage_of_big_words = self.num_of_big_words / self.num_of_words
        self.gunning_fog = (self.avg_sen_len + percentage_of_big_words) * 0.4
        self.gunning_fog = float(f"{self.gunning_fog:.2f}")  # Truncates the result to two decimal places

        # The Flesch Formula
        x = self.avg_sen_len * 1.015
        # print(f"num of words is {self.num_of_words} and number lines is {self.num_of_lines} and x is {x}")
        y = self.num_of_syllables / self.num_of_words * 84.6
        # print(f"{self.num_of_syllables} y is {y}")
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

        #########################################################################################
        # Finally, all of the extra/fun stats are calculated (swear words, drug references, etc.)
        #########################################################################################

        for word in self.swear_words:
            self.num_of_swear_words += self.bare_lyrics.count(word)

        # print("YEET " + str(self.num_of_swear_words))

        to_database(self.full_name, self.lyrics, self.num_of_swear_words, self.num_of_words, self.artist,
                    self.url, self.num_of_jewelery_references, self.num_of_drug_references,
                    self.gunning_fog, self.flesch, self.power_sumner_kearl, self.num_of_adlibs,
                    self.num_of_lines, self.num_of_syllables, self.num_of_big_words, self.avg_sen_len)
