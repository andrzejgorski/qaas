from rest_framework import status
import json
from quiz_creator_front_end_mock.views import with_login
from quiz_creator import models
from django.shortcuts import redirect, render
from quiz_participant import views as rest_views


@with_login
def main_view(request):
    invitations = models.QuizInvitation.objects.filter(email=request.user.email, accepted=False)
    quizzes = models.QuizParticipation.objects.filter(user=request.user)
    content = {
        'invitations': invitations,
        'quizzes': quizzes,
    }
    return render(
        request, "participant/main.html", content
    )


@with_login
def start_quiz(request, quiz_url_id):
    rest_views.start_quiz(request, quiz_url_id)
    return redirect("quiz_question", quiz_url_id=quiz_url_id, question_number=1)


@with_login
def submit_quiz(request, quiz_url_id):
    rest_views.submit_quiz(request, quiz_url_id)
    return redirect("participant_view")


@with_login
def accept_invitation(request, invitation_url_id):
    result = rest_views.accept_invitation(request, invitation_url_id)
    return redirect("participant_view")


def _get_choices(question, participation):
    question_scores = participation.questionscore_set.filter(question=question)
    if len(question_scores) == 1:
        question_score = question_scores[0]
        answers = question_score.singleanswer_set.all()
        result = []
        for answer in answers:
            result.append({
                'text': answer.choice.text,
                'value': answer.value(),
                'number': answer.choice.number,
            })
    elif len(question_scores) == 0:
        result = [
            {
                'text': choice.text,
                'value': False,
                'number': choice.number,
            }
            for choice in question.choice_set.all()
        ]
    else:
        # TODO handle bug
        raise Exception("Data integrity error") 
    return sorted(result, key=lambda x: x['number'])


@with_login
def quiz_question(request, quiz_url_id, question_number):
    if request.method == "GET":
        # TODO validate
        participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
        quiz = participation.quiz

        # TODO change it to quiz.number_of_questions
        number_of_questions = quiz.question_set.count()
        question = quiz.question_set.filter(number=question_number)[0]

        choices = _get_choices(question, participation)
        question_number = int(question_number)

        if question_number != 1:
            prev_question_number = question_number - 1
        else:
            prev_question_number = None

        if question_number != number_of_questions:
            next_question_number = question_number + 1
        else:
            next_question_number = None

        content = {
            'quiz_url_id': quiz_url_id, 
            'question': question,
            'choices': choices,
            'question_number': question_number,
            'prev_question_number': prev_question_number,
            'next_question_number': next_question_number, 
        }
        return render(
            request, "participant/question.html", content
        )
    result = rest_views.answer_question(request, quiz_url_id, question_number)
    if result.status_code != status.HTTP_200_OK:
        return

    next_question_number = request.json.get('next_question_number') or question_number
    return redirect(
        "quiz_question",
        quiz_url_id=quiz_url_id,
        question_number=next_question_number,
    )


@with_login
def all_quizzes(request):
    pass
