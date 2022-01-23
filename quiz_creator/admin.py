from django.contrib import admin

from django.contrib.auth.models import User, Group
from social_django import models as social_models
from . import models


class QuizCreatorAdminSite(admin.AdminSite):
    pass


admin_site = QuizCreatorAdminSite(name='admin')
admin_site.register(models.Question)
admin_site.register(models.QuestionScore)
admin_site.register(models.Quiz)
admin_site.register(models.QuizParticipation)
admin_site.register(models.Choice)
admin_site.register(models.SingleAnswer)
admin_site.register(models.QuizInvitation)

admin_site.register(User)
admin_site.register(Group)

admin_site.register(social_models.Nonce)
admin_site.register(social_models.Association)
admin_site.register(social_models.UserSocialAuth)
