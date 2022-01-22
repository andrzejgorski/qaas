from django.urls import path

from . import views


urlpatterns = [
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('quiz/<quiz_number>/add_question', views.add_question, name='add_question'),
    path('quiz/<quiz_number>/invite', views.invite, name='invite'),
    path('quiz/<quiz_number>/notify/<participation_number>', views.notify, name='notify'),
]
