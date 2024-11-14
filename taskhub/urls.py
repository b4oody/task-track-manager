from django.urls import path
from taskhub.views import (
    get_index_page,
    get_profile,
    sign_up
)

urlpatterns = [
    path("", get_index_page, name="index"),
    path("profile/", get_profile, name="profile"),
    path("register/", sign_up, name="register"),
]

app_name = 'taskhub'
