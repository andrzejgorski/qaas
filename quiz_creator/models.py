from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
import base64
import hashlib
from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    Sum,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    FloatField,
    IntegerField,
    Model,
    PositiveSmallIntegerField,
)


def _get_unique_hash():
    return str(abs(int(hash(datetime.utcnow()))))[:20]


class NumerableModel(Model):
    number = PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True

    @abstractmethod
    def _numerable_query_set(self):
        pass

    def save(self, *args, **kwargs):
        if self.number == 0:
            # next number
            self.number = self._numerable_query_set().count() + 1

        super().save(*args, **kwargs)


class Quiz(NumerableModel):
    created_at = models.DateTimeField(auto_now_add=True)
    user = ForeignKey(User, on_delete=models.CASCADE)
    name = CharField(max_length=50)
    description = CharField(max_length=50)  # CharField(max_length=500)

    def _numerable_query_set(self):
        return self.user.quiz_set

    class Meta:
        indexes = [
            models.Index(fields=['user', 'number',])
        ]

    @classmethod
    def get(cls, number, user):
        quizzes = cls.objects.filter(number=number, user=user)
        if len(quizzes) != 1:
            return None
        return quizzes[0]


class Question(NumerableModel):
    created_at = models.DateTimeField(auto_now_add=True)
    quiz = ForeignKey(Quiz, on_delete=models.CASCADE)
    text = CharField(max_length=500)

    choices = None
    _choices = None

    @property
    def choices(self):
        if not self._choices:
            self._choices = {
                choice.number: choice
                for choice in self.choice_set.all()
            }
        return self._choices

    def get_choice(self, number):
        return self.choices.get(number)

    def _numerable_query_set(self):
        return self.quiz.question_set

    class Meta:
        indexes = [
            models.Index(fields=['quiz', 'number',])
        ]


class QuizParticipation(NumerableModel):
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(default=None, null=True)
    ended_at = models.DateTimeField(default=None, null=True)

    quiz = ForeignKey(Quiz, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)

    started = BooleanField(default=False)
    ended = BooleanField(default=False)
    progress = FloatField(default=0)  # percentage of answered questions
    score = FloatField(default=0)  # 1 for each question
    notified = BooleanField(default=False)

    url_id = models.CharField(max_length=255)

    def start(self):
        self.started = True
        self.started_at = datetime.utcnow()

    def end(self):
        self.ended = True
        self.ended_at = datetime.utcnow()

    def calculate_progress(self):
        answered = self.questionscore_set.count()
        questions = self.quiz.question_set.count()
        if questions != 0:
            self.progress = 100 * answered / questions

    def calculate_score(self):
        result = self.questionscore_set.aggregate(Sum('score'))
        if result.get('score__sum') is not None:
            self.score = result.get('score__sum')

    def _numerable_query_set(self):
        return self.user.quizparticipation_set

    def save(self, *args, **kwargs):
        if self.url_id == '':
            self.url_id = _get_unique_hash()
        self.calculate_progress()
        self.calculate_score()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['url_id']),
            models.Index(fields=['user', 'number',]),
        ]


class QuestionScore(Model):
    created_at = models.DateTimeField(auto_now_add=True)
    quiz_participation = ForeignKey(QuizParticipation, on_delete=models.CASCADE)
    question = ForeignKey(Question, on_delete=models.CASCADE)
    score = FloatField(default=0)

    def calculate_score(self):
        correct_answers = self.singleanswer_set.filter(correct=True).count()
        all_answers = self.singleanswer_set.count()
        if all_answers != 0:
            self.score = correct_answers / all_answers

    def save(self, *args, **kwargs):
        self.calculate_score()
        super().save(*args, **kwargs)


class Choice(NumerableModel):
    question = ForeignKey(Question, on_delete=models.CASCADE)
    text = CharField(max_length=200)
    correct = BooleanField(default=False)

    def _numerable_query_set(self):
        return self.question.choice_set


class SingleAnswer(Model):
    choice = ForeignKey(Choice, on_delete=models.CASCADE)
    question_score = ForeignKey(QuestionScore, on_delete=models.CASCADE)
    correct = BooleanField(default=False)

    def value(self):
        return not (self.correct != self.choice.correct)


class QuizInvitation(Model):
    email = models.EmailField(max_length=255)
    quiz = ForeignKey(Quiz, on_delete=models.CASCADE)

    accepted = BooleanField(default=False)

    @classmethod
    def create_invitations(cls, emails_list, quiz_number, user):
        quiz = Quiz.get(quiz_number, user)
        results = []
        for email in emails_list:
            model = cls(email=email, quiz=quiz)
            model.save()
            results.append(model)
        return results

    url_id = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if self.url_id == '':
            self.url_id = _get_unique_hash()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['url_id']),
            models.Index(fields=['email']),
        ]
