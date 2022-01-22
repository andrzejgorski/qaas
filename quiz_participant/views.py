import json
from rest_framework import status
from rest_framework.response import Response

from quiz_creator import models
from django.shortcuts import render
from . import validate


def accept_invitation(request, invitation_url_id):
    user = request.user

    try:
        invitation = models.QuizInvitation.objects.get(url_id=invitation_url_id)
    except models.QuizInvitation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if invitation.email != user.email:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    if invitation.accepted:
        return Response(status=status.HTTP_410_GONE)

    participations = models.QuizParticipation.objects.filter(quiz=invitation.quiz, user=user)
    if len(participations) > 0:
        # Data integrity error
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    participation = models.QuizParticipation.objects.create(
        quiz=invitation.quiz,
        user=user,
    )
    invitation.accepted = True
    invitation.save()
    return Response(status=status.HTTP_200_OK)


def start_quiz(request, quiz_url_id):
    validation_result = validate.validate_start(request, quiz_url_id)
    if validation_result.status is validate.FAIL:
        return validation_result.response

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    participation.started = True 
    participation.save()
    return Response(status=status.HTTP_200_OK)


def answer_question(request, quiz_url_id, question_number):
    request.json = json.loads(request.body)
    validation_result = validate.validate_question(
        request, quiz_url_id, question_number
    )
    if validation_result.status is validate.FAIL:
        return validation_result.response

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    questions = participation.quiz.question_set.filter(number=question_number)
    if len(questions) != 1:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    question = questions[0]

    # TODO Add handling for already answered questions
    question_scores = question.questionscore_set.filter(
        quiz_participation=participation
    )
    if len(question_scores) == 1:
        created_question_score = False
        question_score = question_scores[0]
    elif len(question_scores) == 0:
        created_question_score = True
        question_score = models.QuestionScore.objects.create(
            quiz_participation=participation,
            question=question,
        )
    else:
        # TODO handle data integrity error
        pass

    answers = request.json.get('answers')
    for answer in answers:
        number = int(answer['number'])
        result = int(answer['result'])

        choice = question.get_choice(number)
        correct = choice.correct == result
        if created_question_score:
            models.SingleAnswer.objects.create(
                choice=choice,
                question_score=question_score,
                correct=correct,
            )
        else:
            answer_model = question_score.singleanswer_set.filter(
                choice__number=number
            )[0]
            answer_model.correct = correct
            answer_model.save()

    question_score.save()
    participation.save()
    return Response(status=status.HTTP_200_OK)


def submit_quiz(request, quiz_url_id):
    validation_result = validate.validate_submit(request, quiz_url_id)
    if validation_result.status is validate.FAIL:
        return validation_result.response

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    participation.ended = True 
    participation.save()
    return Response(status=status.HTTP_200_OK)
    

def all_quizzes(request):
    user = request.user
    pass
