import requests
import re
from django.db import models
from bs4 import BeautifulSoup


# import selenium


# def to_database(title_, lyrics_, swear_words, num_words, artist_, full_artist_, url_, img_url_, header_url_, jewelry_,
#                 drugs_, g,
#                 f, p, adlibs_, lines_, syllables_, big, sentences_):
#     obj = SongDB(title=title_, lyrics=lyrics_, num_of_words=num_words, url=url_, img_url=img_url_,
#                  header_url=header_url_,
#                  num_of_swear_words=swear_words, artist=artist_, full_artists=full_artist_, jewelry=jewelry_,
#                  drugs=drugs_, reading_level_g=g, reading_level_f=f, reading_level_p=p,
#                  adlibs=adlibs_, lines=lines_, syllables=syllables_, big_words=big,
#                  sentence_length=sentences_)
#     obj.save()


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
    primary_artist = models.TextField()
    all_artists = models.TextField()

    lyrics = models.TextField()
    word_count = models.IntegerField()
    swear_words_count = models.IntegerField()
    adlibs = models.IntegerField()
    drug_references = models.IntegerField()
    jewelry_references = models.IntegerField()

    gunning_fog = models.FloatField()
    flesch_kincaid = models.FloatField()
    power_sumner_kearl = models.FloatField()
    avg_grade_level = models.FloatField()

    lines_count = models.IntegerField()
    syllables_count = models.IntegerField()
    big_words_count = models.IntegerField()
    avg_sentence_length = models.IntegerField()

    url = models.URLField()
    img_url = models.URLField()
    header_url = models.URLField()

    def __str__(self):
        return self.title


class Song:
    swear_words = ["fuck", "fucker", "fucked", "motherfucker", "motherfuck", "shit", "bitch", "bitches",
                   "nigga",
                   "niggas", "ass", "cunt", "cunts", "whore", "hoe", "slut", "bastard", "dick", "dicks",
                   "pussy",
                   "sluts", "dickhead", "piss", "asshole", "damn", "goddamn", "titty", "titties", ]

    drugs = ["percs", "percocet", "cocaine", "coco", "xan", "molly", "weed", "drugs", "coke", "lean", "8th",
             "dirty sprite", "codeine", "blunt", "xannie", "acid", "shrooms", "blow", "crack", "powder", "coca",
             "heroin", "420", "broccoli", "cush", "mary jane", "meth", "Act", "addies", "addy", "pop", "remy", "bootch"]

    jewelry = ["patek", "rollie", "chain", "phillipe", "rolex", "diamond", "richard", "millie", "audemars",
               "piguet", "cuban", "cartier", "ice", "icy", "baguettes"]

    def __init__(self, title, artist, lyrics_query):
        # Attributes that the user (can) enter
        self.title = title
        self.primary_artist = artist
        self.lyrics_query = lyrics_query

        # self.full_name = ""  # This is for the name of the song with the artist and any features
        self.all_artists = ""
        self.lyrics = ""  # This holds the original/full text representing the lyrics, meant to be displayed to user
        # self.bare_lyrics = ""
        self.url = ""
        self.img_url = ""
        self.header_url = ""

        # Stats about the song
        self.word_count = 0
        self.swear_words_count = 0
        self.drug_references = 0
        self.jewelry_references = 0
        self.adlibs = 0
        # self.to_add = 0
        # self.gunning_counter = 0
        # self.flesch_counter = 0
        # self.sumner_counter = 0
        # self.drugs_counter = 0
        # self.adlibs_counter = 0

        # The grade level indices
        self.gunning_fog = 0
        self.flesch_kincaid = 0
        self.power_sumner_kearl = 0
        self.avg_grade_level = 0

        # Parameters needs by the indices
        self.lines_count = 0
        self.syllables_count = 0

        self.big_words_count = 0  # The number of words with three or more syllables, used by the indices
        self.avg_sen_len = 0  # The average sentence length

        self.analyze()

    # Besides the original three attributes that the user inputs, this method calculates all of the other stats and
    # indices
    def analyze(self):
        ####################################################
        # First, the song lyrics and the full name are found
        ####################################################
        if '(feat. ' in self.title:
            self.title = self.title[:self.title.index('(feat. ')]
        elif '(ft. ' in self.title:
            self.title = self.title[:self.title.index('(ft. ')]
        elif '(with ' in self.title:
            self.title = self.title[:self.title.index('(with ')]

        song_info = get_song_info(self.title, self.primary_artist, self.lyrics_query)
        if len(song_info["response"]["hits"]) < 1:  # If not hits are there, then return
            self.lyrics = "Song not found. Try searching again."
            return

        song = song_info["response"]["hits"][0]
        full_name = song["result"]["full_title"]
        full_name = full_name.replace(u'\xa0', u' ')  # Take out the weird spaces
        self.title = full_name[:full_name.index(" by ")]

        # Fetches primary artist's name
        self.primary_artist = song["result"]["primary_artist"]["name"]

        try:
            song_db = SongDB.objects.get(title=self.title, primary_artist=self.primary_artist)
            self.lyrics = song_db.lyrics
            self.word_count = song_db.word_count
            self.swear_words_count = song_db.swear_words_count
            self.adlibs = song_db.adlibs
            self.drug_references = song_db.drug_references
            self.jewelry_references = song_db.jewelry_references
            self.gunning_fog = song_db.gunning_fog
            self.flesch_kincaid = song_db.flesch_kincaid
            self.power_sumner_kearl = song_db.power_sumner_kearl
            self.avg_grade_level = song_db.avg_grade_level
            self.lines_count = song_db.lines_count
            self.syllables_count = song_db.syllables_count
            self.big_words_count = song_db.big_words_count
            self.avg_grade_level = song_db.avg_grade_level
            self.avg_sen_len = song_db.avg_sentence_length
            self.url = song_db.url
            self.img_url = song_db.img_url
            self.header_url = song_db.header_url
            print("YEET")
            return
        except SongDB.DoesNotExist:
            pass

        self.all_artists = full_name[full_name.index(" by ") + 4:]
        # Gets the lyrics by passing in the url of the first search result to find_lyrics()
        self.url = song["result"]["url"]
        self.lyrics = find_lyrics(self.url)
        # print("Yeet 2: " + self.lyrics)
        # ALso gets the song's full name

        # Grabs the images for the song
        self.img_url = song["result"]["song_art_image_url"]
        self.header_url = song["result"]["header_image_url"]
        # else:

        self.url = song["result"]["url"]
        # with open("file.json", 'w') as file:
        #     file.write(str(song_info))

        # for hit in song_info["response"]["hits"]:
        #     user_input_name = self.song_title.lower()  # Make the title lowercase for consistency
        #     # print('YEET user input name: ' + user_input_name)
        #     # user_input_name = user_input_name[]
        #     # Remove all extra characters to make comparison easier for user
        #     re.sub('.|(|)|,', '', user_input_name)
        #     print('YEET user input name: ' + user_input_name)
        #
        #     hit_name = hit["result"]["title"].lower()  # Make lowercase
        #     # Remove all extra characters to make comparison easier for user
        #     hit_name = re.sub('[()\u200b.,]', '', hit_name)
        #     # hit_name = re.sub('[()]', '', hit_name)
        #     print("hit name is " + hit_name)
        #
        #     if user_input_name in hit_name:
        #         self.lyrics = find_lyrics(hit["result"]["url"])
        #         full_name = hit["result"]["full_title"]
        #         full_name = full_name.replace(u'\xa0', u' ')  # Take out the weird spaces
        #         self.song_title = full_name[:full_name.index(" by ")].strip()
        #         self.full_artists_names = full_name[full_name.index(" by ") + 4:].strip()
        #         self.url = hit["result"]["url"]
        #
        #         self.artist = hit["result"]["primary_artist"]["name"]
        #         self.img_url = hit["result"]["song_art_image_url"]
        #         self.header_url = hit["result"]["header_image_url"]
        #         break  # Don't delete this line lmao
        # else:
        #     self.lyrics = "Error: Song not found. Check for typos."
        #     return

        #########################################################################
        # Second, the number of lines, words, and syllables of each word is found
        #########################################################################

        lines = self.lyrics.split("\n")
        self.lines_count = len(lines)
        bare_lyrics = ""  # String of all of the words extracted without any new lines, punctuations, or headers
        # ^ Meant to be used in analysis
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
                    self.adlibs += (substring.count(",")) + 1
                except:
                    pass
                num_of_parentheses -= 1

            # Adding only the lines that have lyrics to the variable, bare_lyrics
            if type(line) is None or len(line) == 0 or line[0] == "[":
                self.lines_count -= 1
                continue
            # Only adds lines that are actual lyrics of the song, not headers
            bare_lyrics += line + " "
        # print(f"num of lines{self.num_of_lines}")
        # Removes all non alphanumeric characters from the lyrics
        bare_lyrics = re.sub(r'[^a-zA-Z| |0-9]', "", bare_lyrics)
        bare_lyrics = bare_lyrics.lower()

        # print(bare_lyrics)
        # Makes a list of each individual word
        bare_lyrics_split = bare_lyrics.split()
        self.word_count = len(bare_lyrics_split)  # Counts the number of words in the song

        #######################################################################################################
        # Third, the number of syllables for each word, the total number of syllables, and the average sentence
        # length are calculated, essentially all of the stats needed by the formulas
        #######################################################################################################

        # Creates a set where each lyric only appears once, used to speed up syllable calculations
        lyrics_set = set(bare_lyrics_split)

        # Goes through each word and finds the number of syllables
        syllables_dict = {}  # Dictionary that holds the number of syllables of each word in the song
        for word in lyrics_set:
            syllables_dict[word] = find_syllables(word)
            # greater than three syllables

        for word in bare_lyrics_split:
            if syllables_dict[word] >= 3:
                self.big_words_count += 1  # This is for the Gunning Fog index which needs the number of words that are
            self.syllables_count += syllables_dict[word]

        # print(f"num of big words {self.num_of_big_words}")
        ###########################################################
        # Fourth, the three grade level measurements are calculated
        ###########################################################
        # https://www.tameri.com/teaching/levels.html

        # Gunning Fog index
        self.avg_sen_len = self.word_count / self.lines_count  # Finds the average sentence length
        percentage_of_big_words = self.big_words_count / self.word_count
        self.gunning_fog = (self.avg_sen_len + percentage_of_big_words) * 0.4

        # The Flesch Formula
        x = self.word_count / self.lines_count
        y = self.syllables_count / self.word_count
        self.flesch_kincaid = (0.39 * x) + (11.8 * y) - 15.59

        # x = self.avg_sen_len * 1.015
        # # print(f"num of words is {self.num_of_words} and number lines is {self.num_of_lines} and x is {x}")
        # y = self.syllables_count / self.word_count * 84.6
        # # print(f"{self.num_of_syllables} y is {y}")
        # level = 206.835 - (x + y)
        #
        # if level <= 29:
        #     self.flesch = 'Very difficult Post Graduate'
        # elif level <= 49:
        #     self.flesch = 'Difficult College'
        # elif level <= 59:
        #     self.flesch = 'Fairly Difficult High School'
        # elif level <= 69:
        #     self.flesch = 'Standard 8th to 9th grade'
        # elif level <= 79:
        #     self.flesch = 'Fairly Easy 7th grade'
        # elif level <= 89:
        #     self.flesch = 'Easy 5th to 6th grade'
        # elif level <= 100:
        #     self.flesch = 'Very Easy 4th to 5th grade'
        # else:
        #     self.flesch = 'Below 4th grade lmao'
        # # self.flesch = (150 - level) / 10

        # Power Sumner Kearl
        x = self.word_count / self.lines_count
        # print("num of lines is: " + str(self.num_of_lines))
        y = self.syllables_count
        # print(f"x is{x} and y is {y}")
        y /= (self.word_count / 100)
        # print(f"x is{x} and y is {y}")
        z = (x * 0.0778) + (y * 0.0455)
        self.power_sumner_kearl = z - 2.2029

        self.avg_grade_level = (self.gunning_fog + self.flesch_kincaid + self.power_sumner_kearl) / 3
        self.gunning_fog = float(f"{self.gunning_fog:.2f}")  # Truncates the result to two decimal places
        self.flesch_kincaid = float(f"{self.flesch_kincaid:.2f}")
        self.power_sumner_kearl = float(f"{self.power_sumner_kearl:.2f}")
        self.avg_grade_level = float(f"{self.avg_grade_level:.2f}")

        #########################################################################################
        # Finally, all of the extra/fun stats are calculated (swear words, drug references, etc.)
        #########################################################################################

        for word in self.swear_words:
            self.swear_words_count += bare_lyrics.count(word)

        for word in self.drugs:
            self.drug_references += bare_lyrics.count(word)

        for word in self.jewelry:
            self.jewelry_references += bare_lyrics.count(word)

        # print(self.bare_lyrics)
        # with open("lyrics2.txt", "w") as file:
        #     lines = self.lyrics.split("\n")
        #     for line in lines:
        #         file.write(line + ".\n")

        # if len(currents) == 0:
        #     to_database(self.song_title, self.lyrics, self.num_of_swear_words, self.num_of_words, self.artist,
        #                 self.url, self.img_url, self.header_url, self.num_of_jewelery_references,
        #                 self.num_of_drug_references,
        #                 self.gunning_fog, self.flesch, self.power_sumner_kearl, self.num_of_adlibs,
        #                 self.num_of_lines, self.num_of_syllables, self.num_of_big_words, self.avg_sen_len)

        # currents = SongDB.objects.all()
        # for current in currents:
        #     # check to see if the song already exists in our DB
        #     if current.title == self.title and current.artist == self.primary_artist:
        #         break
        # else:
        song = SongDB(title=self.title, primary_artist=self.primary_artist, all_artists=self.all_artists,
                      lyrics=self.lyrics, word_count=self.word_count, swear_words_count=self.swear_words_count,
                      adlibs=self.adlibs,
                      drug_references=self.drug_references, jewelry_references=self.jewelry_references,
                      gunning_fog=self.gunning_fog, flesch_kincaid=self.flesch_kincaid,
                      power_sumner_kearl=self.power_sumner_kearl,
                      avg_grade_level=self.avg_grade_level, lines_count=self.lines_count,
                      syllables_count=self.syllables_count, big_words_count=self.big_words_count,
                      avg_sentence_length=self.avg_sen_len, url=self.url, img_url=self.img_url,
                      header_url=self.header_url)
        song.save()
        #     to_database(self.title, self.lyrics, self.num_of_swear_words, self.num_of_words, self.primary_artist,
        #                 self.all_artists, self.url, self.img_url, self.header_url,
        #                 self.num_of_jewelery_references, self.num_of_drug_references, self.gunning_fog, self.flesch,
        #                 self.power_sumner_kearl, self.num_of_adlibs, self.num_of_lines, self.num_of_syllables,
        #                 self.num_of_big_words, self.avg_sen_len)
