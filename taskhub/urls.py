from django.urls import path
from taskhub.views import (
    get_index_page,
    get_profile,
    sign_up,
    projects_page_view,
    teams_page_view,
    tasks_page_view,
    create_team_form_view,
    create_project_form_view,
    create_task_form_view,
    CreateTypeView,

)

urlpatterns = [
    path("", get_index_page, name="index"),
    path("profile/", get_profile, name="profile"),
    path("register/", sign_up, name="register"),

    path("profile/projects/", projects_page_view, name="projects"),
    path("profile/create-project/", create_project_form_view, name="create-project"),

    path("profile/teams/", teams_page_view, name="teams"),
    path("profile/create-team/", create_team_form_view, name="create-team"),

    path("profile/tasks/", tasks_page_view, name="tasks"),

    path("profile/create-type/", CreateTypeView.as_view(), name="create-type"),



]

app_name = 'taskhub'
