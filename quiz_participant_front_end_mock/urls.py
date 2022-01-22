from django.urls import path

from . import views


urlpatterns = [
    path('', views.main_view, name='participant_view'),
    path('accept_invitation/<invitation_url_id>', views.accept_invitation, name='accept_invitation'),
    path('<quiz_url_id>/start', views.start_quiz, name='start_quiz'),
    path('<quiz_url_id>/question/<question_number>', views.quiz_question, name='quiz_question'),
    path('<quiz_url_id>/submit', views.submit_quiz, name='submit_quiz'),
    path('my_quizes', views.all_quizzes, name='all_quizzes'),
]
