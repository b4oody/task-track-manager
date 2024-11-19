from django.urls import path
from taskhub.views import (
    get_index_page,
    get_profile,
    sign_up,
    projects_page_view,
    teams_page_view,
    tasks_page_view,
    create_team_form_view,

)

urlpatterns = [
    path("", get_index_page, name="index"),
    path("profile/", get_profile, name="profile"),
    path("register/", sign_up, name="register"),

    path("profile/projects/", projects_page_view, name="projects"),

    path("profile/teams/", teams_page_view, name="teams"),
    path("profile/create-team/", create_team_form_view, name="create-team"),

    path("profile/tasks/", tasks_page_view, name="tasks"),


]

app_name = 'taskhub'
