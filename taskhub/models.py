from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from task_tracker_manager import settings


PRIORITY_CHOICES = [
    ("U", "Urgent"),
    ("H", "High"),
    ("M", "Medium"),
    ("L", "Low"),
]


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
    )

    def __str__(self) -> str:
        return f"{self.username}({self.position}): ({self.first_name} {self.last_name})"


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, default="...Опис команди...")
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="teams",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, default="...Опис проєкта...")
    deadline = models.DateField(db_index=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.name}: ({self.deadline} {self.is_completed})"


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, default="...Опис завдання...")
    deadline = models.DateField(db_index=True)
    is_completed = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(
        max_length=30,
        choices=PRIORITY_CHOICES,
        default="U",
        db_index=True,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",

    )

    class Meta:
        indexes = [
            models.Index(fields=["deadline", "is_completed", "priority"]),
        ]

    def status_display(self):
        return "Completed" if self.is_completed else "In Progress"

    def __str__(self) -> str:
        return f"{self.name} ({self.status_display()})"

    def save(self, *args, **kwargs):
        if self.deadline < timezone.now().date():
            self.is_completed = True
        super().save(*args, **kwargs)
