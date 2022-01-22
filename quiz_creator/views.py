from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import redirect
from django.db.transaction import atomic
from .models import QuizInvitation, Quiz, QuizParticipation
from .forms import QuizForm, QuestionForm, ChoiceFormset, EmailForm
from .smtp_utils import send_invitations, notify_through_email


def create_quiz(request):
    form = QuizForm(request.POST)
    if form.is_valid():
        quiz = form.save(commit=False)
        quiz.user = request.user
        quiz.save()
        content = {
            'quiz_number': quiz.number,
        }
        return Response(content, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@atomic
def save_objects(obj_list):
    for obj in obj_list:
        obj.save()


def add_question(request):
    question_form = QuestionForm(request.POST)
    choice_form = ChoiceFormset(request.POST)
    quiz_number = question_form.data.get('quiz')
    quiz = Quiz.get(quiz_number, request.user)
    if question_form.is_valid() and choice_form.is_valid() and quiz is not None:
        question = question_form.save(commit=False)
        question.quiz = quiz
        objects = [question]
        choices = choice_form.save(commit=False)
        for choice in choices:
            choice.question = question
        objects.extend(choices)
        save_objects(objects)
        return Response(status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def get_quizzes(request):
    quizzes = Quiz.objects.filter(user=request.user)
    content = {
        'quizzes': list(quizzes)
    }
    return Response(content, status=status.HTTP_201_CREATED)


def get_invitations(request, quiz_number):
    quiz = Quiz.get(quiz_number, request.user)
    if quiz is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    invitations = QuizInvitation.objects.filter(
        quiz__number=quiz_number, quiz__user=request.user
    )
    content = {
        'emails': [inv.email for inv in invitations]
    }
    return Response(content, status=status.HTTP_201_CREATED)


def invite(request, quiz_number):
    emails_form = EmailForm(request.POST)     
    if emails_form.is_valid():
        emails_list = EmailForm.sanitize(emails_form.data.get('emails'))
        invitations = QuizInvitation.create_invitations(
            emails_list, quiz_number, request.user
        ) 
        quiz = Quiz.get(quiz_number, request.user)
        if quiz is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        send_invitations(invitations, quiz)   
        return Response(status=status.HTTP_201_CREATED)
       
    error_message = {
        'message': (
            'Invalid emails list. The request should contain list of'
            ' valid email separated by \",\" eg. \"abcd@abcd.com,test@test.com\"'
        )
    }
    return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


def _create_question_result(question_score):
    question = question_score.question
    choices = question.choice_set.all()
    answers = question_score.singleanswer_set.all()
    answers_text_list = []
    for choice, answer in zip(choices, answers):
        if answer.correct:
            your_answer = choice.correct
        else:
            your_answer = not choice.correct
        answers_text_list.append(
            f'{choice.text} [Correct: {choice.correct}] '
            f'[Your answer: {your_answer}]'
        )
    answers_text = "\n".join(answers_text_list)
    return f"""
Question: {question.text}
Score: {question_score.score}
Answers: 
{answers_text}
"""


def _create_notification_message(participation):
    quiz = participation.quiz.name
    score = participation.score
    question_scores = participation.questionscore_set.all()
    questions = "".join(
        _create_question_result(qs)
        for qs in question_scores
    )
    return f"""
This is the email with results from quiz: {quiz}
Your score is: {score}

{questions}
    """


def notify(request, quiz_number, participation_number):
    # TODO add error handling
    quiz = Quiz.get(quiz_number, request.user)
    if quiz is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    participations = (
        QuizParticipation.objects
        .filter(number=participation_number)
        .filter(quiz__number=quiz_number)
        .filter(quiz__user=request.user)
    )
    if len(participations) == 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    participation = participations[0] 
    message = _create_notification_message(participation)
    notify_through_email(message, participation)
    participation.notified = True
    participation.save()
    return Response(status=status.HTTP_201_CREATED)
