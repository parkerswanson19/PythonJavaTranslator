from django.shortcuts import render
from .models import *


# import time


def RapAnalyzerHomePage(request):
    top_lists = getTopLists()
    print(top_lists)
    return render(request, 'rap-analyzer.html', top_lists)


def RapAnalyzerAnalyze(request):
    print("Inside analyze")
    dictionary = getTopLists()
    # t0 = time.clock()
    # Creates a new Song object and assigns it to a local variable
    # 'content' is the name of the first textbox on the HTML page. It's telling Django to take the content of that box,
    # and assign it to the input field in the InputtedCode class
    if len(request.POST['song-name']) == 0 and len(request.POST['artist-name']) == 0 and len(request.POST['lyrics']) \
            == 0:
        print("YEET")
        return render(request, 'rap-analyzer.html')

    new_input = Song(request.POST['song-name'], request.POST['artist-name'], request.POST['lyrics'])

    new_input.analyze()

    dictionary['code'] = new_input

    # t1 = time.clock()
    # print("Time elapsed: ", t1 - t0)  # CPU seconds elapsed (floating point)

    # Re-renders the page and passes the InputtedCode object to the HTML file so the text boxes can be updated
    print("yeet")
    return render(request, 'rap-analyzer2.html', dictionary)


def getTopLists():
    top_lists = {
        'adlibs_list': ["most ad libs", SongDB.objects.order_by('-adlibs')[:4]],
        'swear_words_list': ["most swear words", SongDB.objects.order_by('-num_of_swear_words')[:4]],
        'drug_ref_list': ["most drug references", SongDB.objects.order_by('-drugs')[:4]],
        'jewelery_ref_list': ["most jewelery references", SongDB.objects.order_by('-jewelry')[:4]],
        'high_grade_lvl_list': ["highest grade level", SongDB.objects.order_by('-reading_level_g')[:4]],
        'low_grade_lvl_list': ["lowest grade level", SongDB.objects.order_by('reading_level_g')[:4]],
    }
    return top_lists
