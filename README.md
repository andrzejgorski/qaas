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


###The repository consists of django apps:
    - quiz\_creator (rest application for quiz creator and admin role)
    - quiz\_creator\_front\_end\_mock (mocking views from quiz\_creator with django template)
    - quiz\_participant (rest application for quiz participant role)
    - quiz\_participant\_front\_end\_mock (mocking views from quiz\_participant with django template)
    - user application for user management copied from (https://github.com/sunilale0/django-user-management)

####Other
