from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from taskhub.form import (
    RegistrationForm,
    CreateTeamForm,
    CreateProjectForm, CreateTasksForm,
)
from taskhub.models import (
    Worker,
    Project,
    Position,
    Team,
    Task, TaskType, Commentary
)


def get_index_page(request: HttpRequest) -> HttpResponse:
    return render(request, "index/index.html")


def sign_up(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.position = form.cleaned_data["position"]
            worker.save()
            login(request, worker)
            return redirect("taskhub:profile")
    else:
        form = RegistrationForm()
    positions = Position.objects.all()
    return render(
        request,
        "registration/register.html",
        {"form": form, "positions": positions})


@login_required
def get_profile(request: HttpRequest) -> HttpResponse:
    worker = Worker.objects.prefetch_related("teams", "tasks").get(pk=request.user.id)
    tasks = worker.tasks.aggregate(
        active_tasks=Count("id", filter=Q(is_completed=False)),
        finished_tasks=Count("id", filter=Q(is_completed=True)),
    )
    finished_projects_count = Project.objects.filter(
        Q(team__in=worker.teams.all()), Q(is_completed=True)
    ).count()
    context = {
        "worker": worker,
        "active_tasks": tasks["active_tasks"],
        "finished_projects": finished_projects_count,
        "finished_tasks": tasks["finished_tasks"],
    }

    return render(request, "profile/profile.html", context=context)


def projects_page_view(request: HttpRequest) -> HttpResponse:
    worker = Worker.objects.get(pk=request.user.id)
    worker_projects = Project.objects.filter(
        team__in=worker.teams.all()
    ).select_related("team").prefetch_related("team__members")
    context = {
        "worker_projects": worker_projects,
    }
    return render(request, "projects/projects.html", context=context)


def teams_page_view(request: HttpRequest) -> HttpResponse:
    worker = Worker.objects.get(pk=request.user.id)
    context = {
        "worker_teams": Team.objects.filter(members=worker)
    }
    return render(request, "teams/user-teams.html", context=context)


def tasks_page_view(request: HttpRequest) -> HttpResponse:
    worker = Worker.objects.get(pk=request.user.id)
    context = {
        "worker_tasks": Task.objects.filter(assignees=worker)
    }
    return render(request, "tasks/tasks.html", context=context)


def create_team_form_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("taskhub:teams")
    else:
        form = CreateTeamForm()
    return render(
        request,
        "profile/create_team_form.html",
        context={"form": form}
    )


def create_project_form_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("taskhub:projects")
    else:
        form = CreateProjectForm()
    return render(
        request,
        "profile/create_project_form.html",
        context={"form": form}
    )


class CreateTypeView(generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "tasks/create_type_form.html"
    success_url = reverse_lazy("taskhub:tasks")

    def form_valid(self, form):
        response = super().form_valid(form)
        referer = self.request.POST.get("referer", None)
        if referer:
            return HttpResponseRedirect(referer)
        return response


def create_task_form_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CreateTasksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("taskhub:tasks")
    else:
        form = CreateTasksForm()
    return render(
        request,
        "profile/create_task_form.html",
        context={"form": form}
    )


def task_details_page_view(request: HttpRequest, pk: int) -> HttpResponse:
    task = (
        Task.objects.select_related("project__team", "task_type")
        .prefetch_related("assignees", "assignees__position", "commentaries__worker")
        .get(pk=pk)
    )
    context = {
        "task": task,
    }
    return render(
        request,
        "tasks/task-details.html",
        context
    )
