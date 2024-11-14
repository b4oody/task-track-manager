from django.urls import path
from taskhub.views import (
    get_index_page,
)

urlpatterns = [
    path("", get_index_page, name="index"),
]

app_name = 'taskhub'
