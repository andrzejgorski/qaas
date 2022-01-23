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
