import time

from django.shortcuts import render
from .models import *
from .RapCaviar import pull_from_spotify_playlist


def RapAnalyzerHomePage(request):
    dictionary = getTopLists()
    # print(top_lists)
    return render(request, 'rap-analyzer.html', dictionary)


def RapAnalyzerAnalyze(request):
    # for i in range(0, 10): # Do not uncomment these two lines
    #     pull_from_spotify_playlist(i * 100)
    dictionary = getTopLists()

    t0 = time.clock()
    # Creates a new Song object and assigns it to a local variable
    # 'content' is the name of the first textbox on the HTML page. It's telling Django to take the content of that box,
    # and assign it to the input field in the InputtedCode class
    if len(request.POST['song-name']) == 0 and len(request.POST['artist-name']) == 0 and len(request.POST['lyrics']) \
            == 0:
        return render(request, 'rap-analyzer.html', dictionary)

    new_input = Song(request.POST['song-name'], request.POST['artist-name'], request.POST['lyrics'])

    dictionary['code'] = new_input

    t1 = time.clock()
    print("Time elapsed: ", t1 - t0)  # CPU seconds elapsed (floating point)

    dict_tops = {"top_sumner": order_by('reading_level_p'),"top_flesch": order_by('reading_level_f'),
                 "top_gunning": order_by('reading_level_g'), "top_drugs": order_by('drugs'),
                 "top_adlibs": order_by('adlibs'), "top_jewelry": order_by('jewelry')}

    # Re-renders the page and passes the InputtedCode object to the HTML file so the text boxes can be updated
    return render(request, 'rap-analyzer2.html', dictionary)


def getTopLists():
    top_lists = {
        'adlibs_list': ["most ad libs", SongDB.objects.order_by('-adlibs')[:4]],
        'swear_words_list': ["most swear words", SongDB.objects.order_by('-swear_words_count')[:4]],
        'drug_ref_list': ["most drug references", SongDB.objects.order_by('-drug_references')[:4]],
        'jewelery_ref_list': ["most jewelery references", SongDB.objects.order_by('-jewelry_references')[:4]],
        'high_grade_lvl_list': ["highest grade level", SongDB.objects.order_by('-avg_grade_level')[:4]],
        'low_grade_lvl_list': ["lowest grade level", SongDB.objects.order_by('avg_grade_level')[:4]],
    }
    return top_lists

