from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from taskhub.form import RegistrationForm
from taskhub.models import Worker, Project, Position


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
        team__in=worker.teams.all()
    ).distinct().count()
    context = {
        "worker": worker,
        "active_tasks": tasks["active_tasks"],
        "finished_projects": finished_projects_count,
        "finished_tasks": tasks["finished_tasks"],
    }

    return render(request, "profile/profile.html", context=context)
