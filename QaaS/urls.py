from django.conf.urls import include, url


urlpatterns = [
    url(r"^", include("users.urls")),
    url(r'^quiz_creator/', include('quiz_creator_front_end_mock.urls')),
    url(r'^quiz/', include('quiz_participant_front_end_mock.urls')),
    url(r"^admin/", include('quiz_creator.admin_urls')),
]
