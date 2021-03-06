from django.urls import path

from . import views

urlpatterns = [
    path('', views.RapAnalyzerHomePage, name='homePage'),  # If at homepage, call index method in views py script
    path('stat/<str:title>/<str:artist>/', views.viewStatSong, name='stat'),
    path('analyze/', views.RapAnalyzerAnalyze)  # If translate button pressed, call index method in views py script


]