from django.urls import path

from . import views


urlpatterns = [
    path('quiz/accept_invitation/<invitation_url_id>', views.accept_invitation, name='accept_invitation'),
    path('quiz/<participation_url_id>/start', views.start_quiz, name='start_quiz'),
    path('quiz/<participation_url_id>/submit', views.submit_quiz, name='submit_quiz'),
    path('quiz/<participation_url_id>/question', views.answer_question, name='answer_question'),
    path('quiz/my_quizes', views.all_quizzes, name='all_quizzes'),
]
