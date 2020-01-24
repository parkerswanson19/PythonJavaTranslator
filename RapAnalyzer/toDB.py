from .models import SongDB

def to_database(title_, lyrics_, swear_words, num_words, artist_, url_):
    obj = SongDB(title = title_, lyrics = lyrics_, num_of_words = num_words, url = url_,
                 num_of_swear_words = swear_words, artist = artist_)
    obj.save()