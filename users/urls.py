from django.conf.urls import url, include
from users.views import dashboard, register, main_view

urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^dashboard/", dashboard, name="dashboard"),
    url(r"^oauth/", include("social_django.urls")),
    url(r"^register/", register, name="register"),
    url(r"^$", main_view, name="quiz_creator_direct"),
]
