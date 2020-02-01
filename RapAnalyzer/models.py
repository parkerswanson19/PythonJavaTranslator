import requests
import re
from django.db import models
from bs4 import BeautifulSoup


def to_database(title_, lyrics_, swear_words, num_words, artist_, full_artist_, url_, img_url_, header_url_, jewelry_,
                drugs_, g,
                f, p, adlibs_, lines_, syllables_, big, sentences_):
    obj = SongDB(title=title_, lyrics=lyrics_, num_of_words=num_words, url=url_, img_url=img_url_,
                 header_url=header_url_,
                 num_of_swear_words=swear_words, artist=artist_, full_artists=full_artist_, jewelry=jewelry_,
                 drugs=drugs_, reading_level_g=g, reading_level_f=f, reading_level_p=p,
                 adlibs=adlibs_, lines=lines_, syllables=syllables_, big_words=big,
                 sentence_length=sentences_)
    obj.save()


def find_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    lyrics = soup.find('div', class_='lyrics').get_text()
    return lyrics


def order_by(category):
    objs = SongDB.objects.order_by(category)
    if len(objs) >= 10:
        return objs[:10]
    else:
        return objs


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
    title = models.TextField()
    artist = models.TextField()
    full_artists = models.TextField()
    lyrics = models.TextField()
    num_of_words = models.IntegerField()
    num_of_swear_words = models.IntegerField()
    url = models.URLField()
    img_url = models.URLField()
    header_url = models.URLField()
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

    drugs = ["percs", "percocet", "cocaine", "coco", "xan", "molly", "weed", "drugs", "coke", "lean", "8th",
             "dirty sprite",  "codeine", "blunt", "xannie", "acid", "shrooms", "blow", "crack", "powder", "coca",
             "heroin", "420", "broccoli", "cush", "mary jane", "meth", "Act", "addies", "addy", "pop", "remy", "bootch"]

    jewelery = ["patek", "rollie", "chain", "phillipe", "rolex", "diamond", "richard", "millie", "audemars", "piguet"
        , "cuban", "cartier", "ice", "icy", "baguettes"]

    def __init__(self, song_title, artist, lyrics_query):
        # Attributes that the user (can) enter
        self.song_title = song_title
        self.artist = artist
        self.lyrics_query = lyrics_query

        # self.full_name = ""  # This is for the name of the song with the artist and any features
        self.full_artists_names = ""
        self.lyrics = ""  # This holds the original/full text representing the lyrics, meant to be displayed to user
        self.bare_lyrics = ""  # String of all of the words extracted without any new lines, punctuations, or headers
        # ^ Meant to be used in analysis
        self.url = ""
        self.img_url = ""
        self.header_url = ""

        # Stats about the song
        self.num_of_words = 0
        self.num_of_swear_words = 0
        self.num_of_drug_references = 0
        self.num_of_jewelery_references = 0
        self.num_of_adlibs = 0
        # self.to_add = 0
        # self.gunning_counter = 0
        # self.flesch_counter = 0
        # self.sumner_counter = 0
        # self.drugs_counter = 0
        # self.adlibs_counter = 0

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
            self.url = song_info["response"]["hits"][0]["result"]["url"]
            self.lyrics = find_lyrics(self.url)

            # ALso gets the song's full name
            full_name = song_info["response"]["hits"][0]["result"]["full_title"]
            full_name = full_name.replace(u'\xa0', u' ')  # Take out the weird spaces
            self.song_title = full_name[:full_name.index(" by ")]
            self.full_artists_names = full_name[full_name.index(" by ") + 4:]

            # Fetches primary artist's name
            self.artist = song_info["response"]["hits"][0]["result"]["primary_artist"]["name"]

            self.img_url = song_info["response"]["hits"][0]["result"]["url"]
        else:
            song_info = get_song_info(self.song_title, self.artist)
            self.url = song_info["response"]["hits"][0]["result"]["url"]
            # with open("file.json", 'w') as file:
            #     file.write(str(song_info))

            for hit in song_info["response"]["hits"]:
                user_input_name = self.song_title.lower()  # Make the title lowercase for consistency

                # Remove all extra characters to make comparison easier for user
                user_input_name = re.sub('.|\(|\)|,', '', user_input_name)

                hit_name = hit["result"]["title"].lower()  # Make lowercase
                # Remove all extra characters to make comparison easier for user
                hit_name = re.sub('.|\(|\)|,|\u200b', '', hit_name)

                if user_input_name in hit_name:
                    self.lyrics = find_lyrics(hit["result"]["url"])
                    full_name = hit["result"]["full_title"]
                    full_name = full_name.replace(u'\xa0', u' ')  # Take out the weird spaces
                    self.song_title = full_name[:full_name.index(" by ")].strip()
                    self.full_artists_names = full_name[full_name.index(" by ") + 4:].strip()

                    self.artist = hit["result"]["primary_artist"]["name"]
                    self.img_url = hit["result"]["song_art_image_url"]
                    self.header_url = hit["result"]["header_image_url"]
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
            line_copy = line
            # Counting the number of parentheses to find the number of adlibs
            num_of_parentheses = line_copy.count('(')
            index_2 = 0
            while num_of_parentheses > 0:
                try:
                    index = line_copy.index("(")
                    index_2 = line_copy.index(")")
                    substring = line_copy[index + 1: index_2]
                    line_copy = line_copy[index_2 + 1:]
                    self.num_of_adlibs += (substring.count(",")) + 1
                except:
                    pass
                num_of_parentheses -= 1

            # Adding only the lines that have lyrics to the variable, bare_lyrics
            if type(line) is None or len(line) == 0 or line[0] == "[":
                self.num_of_lines -= 1
                continue
            # Only adds lines that are actual lyrics of the song, not headers
            self.bare_lyrics += line + " "
        # print(f"num of lines{self.num_of_lines}")
        # Removes all non alphanumeric characters from the lyrics
        self.bare_lyrics = re.sub(r'[^a-zA-Z| |0-9]', "", self.bare_lyrics)
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

        # print(f"num of big words {self.num_of_big_words}")
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

        for word in self.drugs:
            self.num_of_drug_references += self.bare_lyrics.count(word)

        for word in self.jewelery:
            self.num_of_jewelery_references += self.bare_lyrics.count(word)

        # print(self.bare_lyrics)
        # with open("lyrics2.txt", "w") as file:
        #     lines = self.lyrics.split("\n")
        #     for line in lines:
        #         file.write(line + ".\n")

        currents = SongDB.objects.all()

        # if len(currents) == 0:
        #     to_database(self.song_title, self.lyrics, self.num_of_swear_words, self.num_of_words, self.artist,
        #                 self.url, self.img_url, self.header_url, self.num_of_jewelery_references,
        #                 self.num_of_drug_references,
        #                 self.gunning_fog, self.flesch, self.power_sumner_kearl, self.num_of_adlibs,
        #                 self.num_of_lines, self.num_of_syllables, self.num_of_big_words, self.avg_sen_len)

        for current in currents:
            # check to see if the song already exists in our DB
            if current.title == self.song_title and current.artist == self.artist:
                break
        else:
            to_database(self.song_title, self.lyrics, self.num_of_swear_words, self.num_of_words, self.artist,
                        self.full_artists_names, self.url, self.img_url, self.header_url,
                        self.num_of_jewelery_references, self.num_of_drug_references, self.gunning_fog, self.flesch,
                        self.power_sumner_kearl, self.num_of_adlibs, self.num_of_lines, self.num_of_syllables,
                        self.num_of_big_words, self.avg_sen_len)

        #     if self.gunning_fog < current.reading_level_g:
        #         self.gunning_counter += 1
        #     if self.flesch < current.reading_level_f:
        #         self.flesch_counter += 1
        #     if self.power_sumner_kearl < current.reading_level_p:
        #         self.sumner_counter += 1
        #     if self.num_of_drug_references < current.drugs:
        #         self.drugs_counter += 1
        #     if self.num_of_adlibs < current.adlibs:
        #         self.adlibs_counter += 1
        #
        # if self.gunning_counter <= 10:
        #     self.to_add += 1
        # if self.sumner_counter <= 10:
        #     self.to_add += 1
        # if self.flesch_counter <= 10:
        #     self.to_add += 1
        # if self.drugs_counter <= 10:
        #     self.to_add += 1
        # if self.adlibs_counter <= 10:
        #     self.to_add += 1

        # if self.to_add > 0:

        # to_database(self.full_name, self.lyrics, self.num_of_swear_words, self.num_of_words, self.artist,
        #             self.url, self.num_of_jewelery_references, self.num_of_drug_references,
        #             self.gunning_fog, self.flesch, self.power_sumner_kearl, self.num_of_adlibs,
        #             self.num_of_lines, self.num_of_syllables, self.num_of_big_words, self.avg_sen_len)
