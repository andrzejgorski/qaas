from collections import namedtuple
from quiz_creator import models
from rest_framework import status
from rest_framework.response import Response


ValidationResult = namedtuple("ValidationResult", ["status", "response"])
OK = 1
FAIL = 0


def _not_found():
    return ValidationResult(
        FAIL,
        Response(status=status.HTTP_404_NOT_FOUND)
    )


def _invalid_user():
    return ValidationResult(
        FAIL,
        Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    )


def _ok_request():
    return ValidationResult(OK, None)


def _bad_request(message=None):
    content = {}
    if message:
        content['message'] = message
    return ValidationResult(FAIL, 
            Response(content, status=status.HTTP_400_BAD_REQUEST))


def _validate_participation(request, quiz_url_id):
    try:
        participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    except models.QuizParticipation.DoesNotExist:
        return _not_found()

    if participation.user != request.user:
        return _invalid_user()

    return _ok_request()


def _validate_url_id(request, quiz_url_id):
    validation_result = _validate_participation(request, quiz_url_id)
    if validation_result.status == FAIL:
        return validation_result
    return _ok_request()


def validate_start(request, quiz_url_id):
    validation_result = _validate_participation(request, quiz_url_id)
    if validation_result.status == FAIL:
        return validation_result

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    if participation.started:
        return _bad_request()

    return _ok_request()


def validate_submit(request, quiz_url_id):
    validation_result = _validate_participation(request, quiz_url_id)
    if validation_result.status == FAIL:
        return validation_result

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    if participation.ended:
        return _bad_request()

    return _ok_request()


def validate_question(request, quiz_url_id, question_number):
    validation_result = _validate_participation(request, quiz_url_id)
    if validation_result.status == FAIL:
        return validation_result

    participation = models.QuizParticipation.objects.get(url_id=quiz_url_id)
    try:
        question = models.Question.objects.get(
            number=question_number,
            quiz=participation.quiz
        )
    except models.Question.DoesNotExist:
        return _not_found()

    answers = request.json.get('answers')
    if answers is None:
        return _bad_request()

    if len(answers) != question.choice_set.count():
        return _bad_request('Wrong Number of Choices')

    for answer in answers:
        number = int(answer.get('number'))
        if question.get_choice(number) is None:
            return _bad_request(f'Choice with number {number} does not exists')

        result = bool(answer.get('result'))
        if not (result is True or result is False):
            return _bad_request(f'Answer result could be only [true] or [false] not [{result}]')
            
    return _ok_request()
