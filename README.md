# qaas

Application for building and hosting quizzes (simple multiple-choice with question and answers) that can be solved by using an API.

Functionalities as Quiz Creator:
- Building a quiz
- Invitie quiz participants through e-mail
- Check up on the progress of the quiz
- Check up on the scores of the quiz
- Notify participants of the result through e-mail

Functionalities as Quiz User:
- Accept an invitation
- Participate in the quiz
- Check up on the progress of the quiz

Functionalities as Admin:
- django admin panel
- daily report on usage


The repository consists of django apps:

    - quiz_creator (rest application for quiz creator and admin role)
    - quiz_creator_front_end_mock (mocking views from quiz_creator with django template)
    - quiz_participant (rest application for quiz participant role)
    - quiz_participant_front_end_mock (mocking views from quiz_participant with django template)
    - user application for user management copied from (https://github.com/sunilale0/django-user-management)

Other:
1. quiz_creator_front_end_mock uses django forms for generating forms
2. quiz_participant_front_end_mock users very oldschool js script in django template
3. quie_creator_front_end_mock contains file fake_data.py. If you're bored with adding data to test manually you can use it:
`python manage.py shell` and run `from quiz_creator_front_end_mock import fake_data; fake_data.create_fake_data()` and login for users:
`fake_user` and `fake_quiz_creator` using `abcd` password.

How to run?
```bash
# 1. make sure you have installed virtualenv wrapper and run
mkvirutalenv qaas

# than
pip install -r requirements.txt
# Make sure you have running postgres on you laptop. Type 'sudo -u postgres pqsl' to check. If you don't want you can change your db to sqllite.
# Create database "quizdb" on your workstation and make sure you granted your user all privileges to them.
# You can inspire by DB_create file (which contains bash scripts)
# make sure you have running smtp server
python manage.py makemigrations quiz_creator
python manage.py migrate

python manage.py runserver  # for running application. Now you can go to http://localhost:8000
python manage.py test
```

Tested on python 3.9 and django 3.2
