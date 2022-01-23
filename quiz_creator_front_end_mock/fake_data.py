import random
 
 
def create_fake_user(username, email=None):
    from django.contrib.auth.models import User

    email = email or 'fake@email.com'
    password = 'abcd'
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


def create_fake_questions(quiz):
    question_text_tmp = "Fake Quiz Question"
    from quiz_creator import models

    for question_number in range(5):
        question_text = f"{question_text_tmp} {question_number}"
        question = models.Question.objects.create(
            quiz=quiz,
            text=question_text,
        )

        for i in range(5):
            choice = models.Choice.objects.create(
                question=question,
                text=f"{question_text} Choice {i}",
                correct=random.choice([True, False]),
            )


def create_fake_invitation(quiz):
    from quiz_creator import models
    for i in range(5):
        invitation = models.QuizInvitation.objects.create(
            email=f'fakeemail{i}@email.com',
            quiz=quiz,
        )


def create_fake_quiz(quiz_name):
    from quiz_creator import models
    fake_quiz_creator = create_fake_user(
        'fake_quiz_creator',
        email='fakequizcreator@email.com',
    )

    quiz = models.Quiz.objects.create(
        user=fake_quiz_creator, 
        name=quiz_name,
        description="Fake quiz",
    )
    create_fake_questions(quiz)
    create_fake_invitation(quiz)
    return quiz


def create_fake_participation(quiz=None, user=None, started=True, ended=True):
    from quiz_creator import models
    if quiz is None:
        quizzes = models.Quiz.objects.filter(name="Fake Quiz")
        if len(quizzes) == 1:
            quiz = quizzes[0]
        else:
            raise Exception("There is Fake Quiz. Create it before creating participation")

    fake_user = user or create_fake_user('fake_user', email='fake_user@email.com')
    participation = models.QuizParticipation.objects.create(
        quiz=quiz,
        user=fake_user,
    )
    if started:
        for question in quiz.question_set.all():
            question_score = models.QuestionScore.objects.create(
                quiz_participation=participation,
                question=question,
            )
            for choice in question.choice_set.all():
                answer = models.SingleAnswer.objects.create(
                    choice=choice,
                    question_score=question_score,
                    correct=random.choice([True, False])
                )
            question_score.save()

    participation.started = started
    participation.ended = ended
    participation.save()


def create_fake_data():
    # Delete fake quiz creator to clear data:
    from django.contrib.auth.models import User
    User.objects.filter(username='fake_quiz_creator').delete()

    from quiz_creator import models
    finished_quiz = create_fake_quiz("Fake Quiz Finished")
    fake_user = create_fake_user('fake_user', email='fake_user@email.com')
    create_fake_participation(finished_quiz, fake_user, started=True, ended=True)

    started_quiz = create_fake_quiz("Fake Quiz Started")
    create_fake_participation(started_quiz, fake_user, started=True, ended=False)

    not_started_quiz = create_fake_quiz("Fake Quiz Not Started")
    create_fake_participation(not_started_quiz, fake_user, started=False, ended=False)

    invited_quiz = create_fake_quiz("Invited Quiz")
    models.QuizInvitation.objects.create(
        email=fake_user.email,
        quiz=invited_quiz,
    )
