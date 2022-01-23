from django.urls import path
from django.conf.urls import url
from quiz_creator import admin
from quiz_creator.views import report


urlpatterns = [
    path('report/', admin.admin_site.admin_view(report), name='report'),
    url(r'', admin.admin_site.urls),
]
