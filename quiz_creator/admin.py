from django.contrib import admin

from . import models


admin.site.register(models.Question)
admin.site.register(models.QuestionScore)
admin.site.register(models.Quiz)
admin.site.register(models.QuizParticipation)
admin.site.register(models.Choice)
admin.site.register(models.SingleAnswer)
admin.site.register(models.QuizInvitation)
