from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models import Q as djangoQuery
from quiz_creator.forms import QuizForm
from quiz_creator_front_end_mock.forms import QuestionForm, ChoiceFormset, EmailForm
from quiz_creator.models import Quiz, QuizInvitation, QuizParticipation
from quiz_creator import views as rest_views


def with_login(fn):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login")
        return fn(request, *args, **kwargs)
    return wrapped


@with_login
def create_quiz(request):
    if request.method == "GET":
        return render(
            request, "creator/create_quiz.html",
            {"form": QuizForm}
        )
    elif request.method == "POST":
        response = rest_views.create_quiz(request) 
        if response.status_code == status.HTTP_201_CREATED:
            return redirect("add_question", quiz_number=response.data['quiz_number'])
        # TODO add bad request info
        return redirect("index")


@with_login
def add_question(request, quiz_number):
    if request.method == "GET":
        question_form = QuestionForm(initial={'quiz': int(quiz_number)})
        answer_form = ChoiceFormset()
        return render(
            request, "creator/create_question.html",
            {
                "question_form": question_form,
                "answer_form": answer_form,
            }
        )
    elif request.method == "POST":
        response = rest_views.add_question(request) 
        if response.status_code == status.HTTP_201_CREATED:
            return redirect("add_question", quiz_number=quiz_number)
        # TODO add bad request info
        return redirect("index")


@with_login
def invite(request, quiz_number):
    if request.method == "GET":
        return render(
            request, "creator/invite.html"
        )
    elif request.method == "POST":
        response = rest_views.add_question(request) 
        if response.status_code == status.HTTP_201_CREATED:
            return redirect("add_question", quiz_number=quiz_number)
        # TODO add bad request info
        return redirect("index")


@with_login
def quizzes(request):
    quizzes = Quiz.objects.filter(user=request.user)
    context = {
        'quizzes': list(quizzes)
    }
    return render(request, "creator/quizzes.html", context)


@with_login
def index(request):
    return render(request, "creator/main.html")


@with_login
def invite(request, quiz_number):
    if request.method == "GET":
        quiz = Quiz.get(quiz_number, request.user)
        if quiz is None:
            return redirect("quiz", quiz_number=quiz_number)

        context = {
            'form': EmailForm(),
            'quiz': quiz.name,
        }
        return render(
            request, "creator/invite.html", context
        )
    elif request.method == "POST":
        response = rest_views.invite(request, quiz_number) 
        if response.status_code == status.HTTP_201_CREATED:
            return redirect("quiz", quiz_number=quiz_number)
        # TODO add bad request info
        return redirect("quiz", quiz_number=quiz_number)


@with_login
def quiz(request, quiz_number):
    if request.method == "GET":
        user = request.user
        quiz = Quiz.get(quiz_number, request.user)
        if quiz is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        invited = [
            invitation.email
            for invitation in 
            QuizInvitation.objects.filter(quiz__number=quiz_number, quiz__user=user)
            .filter(accepted=False)
        ]

        participations = [
            {
                'email': participation.user,
                'progress': participation.progress,
                'score': participation.score,
                'number': participation.number,
                'notified': participation.notified,
            }
            for participation in QuizParticipation.objects.filter(quiz__number=quiz_number, quiz__user=user)
        ]

        context = {
            'quiz': quiz, 
            'participations': participations,
            'invited': invited,
        }

        return render(request, "creator/quiz.html", context)
        
    return Response(status=status.HTTP_404_NOT_FOUND)


@with_login
def notify(request, quiz_number, participation_number):
    response = rest_views.notify(request, quiz_number, participation_number)
    return redirect("quiz", quiz_number=quiz_number)
