from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # If at homepage, call index method in views py script
    path('translate/', views.takeInput)  # If translate button pressed, call index method in views py script
]