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

    task_details_page_view,
    team_details_page_view,
    project_details_page_view,

    AddNewMemberToTeam,
    DeleteMemberFromTeam,
    DeleteProjectView,
    DeleteTaskView,

)

urlpatterns = [
    path("", get_index_page, name="index"),
    path("profile/", get_profile, name="profile"),
    path("register/", sign_up, name="register"),


    path("profile/projects/", projects_page_view, name="projects"),
    path("profile/create-project/", create_project_form_view, name="create-project"),
    path("profile/project/delete/<int:pk>/", DeleteProjectView.as_view(), name="delete-project"),
    path("profile/project/<int:pk>/", project_details_page_view, name="project-details"),


    path("profile/teams/", teams_page_view, name="teams"),
    path("profile/create-team/", create_team_form_view, name="create-team"),
    path("profile/team/<int:pk>/", team_details_page_view, name="team-details"),
    path("profile/team/<int:pk>/add-member/", AddNewMemberToTeam.as_view(), name="add-member"),
    path(
        "profile/team/<int:team_pk>/delete/<int:member_pk>/",
        DeleteMemberFromTeam.as_view(),
        name="delete-member"
    ),


    path("profile/tasks/", tasks_page_view, name="tasks"),
    path("profile/create-task/", create_task_form_view, name="create-task"),
    path("profile/create-type/", CreateTypeView.as_view(), name="create-type"),
    path("profile/task/<int:pk>/", task_details_page_view, name="task-detail"),
    path("profile/delete/<int:pk>/", DeleteTaskView.as_view(), name="task-delete"),


]

app_name = 'taskhub'
