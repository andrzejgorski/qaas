from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='creator_view'),
    path('create_quiz', views.create_quiz, name='create_quiz'),
    path('quizzes', views.quizzes, name='quizzes'),
    path('quiz/<quiz_number>', views.quiz, name='quiz'),
    path('quiz/<quiz_number>/add_question', views.add_question, name='add_question'),
    path('quiz/<quiz_number>/invite', views.invite, name='invite'),
    path('quiz/<quiz_number>/notify/<participation_number>', views.notify, name='notify'),
]
