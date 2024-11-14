from django.urls import path
from taskhub.views import (
    get_index_page,
    sign_up
)

urlpatterns = [
    path("", get_index_page, name="index"),
    path("register/", sign_up, name="register"),
]

app_name = 'taskhub'
