import copy
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User
from django.test import TestCase

from quiz_creator import models
from quiz_creator import views


class QuizCreator(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory(encorce_csrf_checks=True)
        self.user = User.objects.create(username='test_user')


class TestCreateQuiz(QuizCreator):
    def test_create_quiz(self):
        self.assertEqual(models.Quiz.objects.count(), 0)
        request = self.factory.post(
            'create_quiz',
            {
                'name': 'Quiz name',
                'description': 'Quiz Description'
            }
        )
        force_authenticate(request, user=self.user)
        result = views.create_quiz(request)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Quiz.objects.count(), 1)

    def test_create_quiz_bad_request(self):
        self.assertEqual(models.Quiz.objects.count(), 0)
        request = self.factory.post('create_quiz', {})
        result = views.create_quiz(request)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Quiz.objects.count(), 0)


class TestAddQuestion(QuizCreator):
    def setUp(self):
        super().setUp()
        self.quiz = models.Quiz.objects.create(
            name='name',
            description='description',
            user=self.user,
        )
        self.init_body = {
            'text': 'question_text',
            'quiz': self.quiz.number,
            'choice_set-INITIAL_FORMS': '0',
            'choice_set-MIN_NUM_FORMS': '0',
            'choice_set-MAX_NUM_FORMS': '1000',
        }
        self.url = f'quiz/{self.quiz.number}/add_question'

    def _get_request_body(self, choices=1):
        body = copy.deepcopy(self.init_body)
        for i in range(0, choices):
            body.update({
                f'choice_set-{i}-text': 'choice text',
                f'choice_set-{i}-correct': 'on',
                f'choice_set-{i}-id': '',
                f'choice_set-{i}-question': '',
            })
        body['choice_set-TOTAL_FORMS'] = str(choices)
        return body

    def test_add_question_one_choice(self):
        self.assertEqual(models.Question.objects.count(), 0)
        self.assertEqual(models.Choice.objects.count(), 0)
        body = self._get_request_body(choices=1)
        request = self.factory.post(self.url, body)
        force_authenticate(request, user=self.user)

        result = views.add_question(request)
        self.assertEqual(models.Question.objects.count(), 1)
        self.assertEqual(models.Choice.objects.count(), 1)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_add_question_bad_request(self):
        self.assertEqual(models.Question.objects.count(), 0)
        request = self.factory.post(self.url, {})
        force_authenticate(request, user=self.user)

        result = views.add_question(request)
        self.assertEqual(models.Question.objects.count(), 0)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_question_many_choice(self):
        choices_number = 16
        self.assertEqual(models.Question.objects.count(), 0)
        self.assertEqual(models.Choice.objects.count(), 0)
        body = self._get_request_body(choices=choices_number)
        request = self.factory.post(self.url, body)
        force_authenticate(request, user=self.user)

        result = views.add_question(request)
        self.assertEqual(models.Question.objects.count(), 1)
        self.assertEqual(models.Choice.objects.count(), choices_number)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
