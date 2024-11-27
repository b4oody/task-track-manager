from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404

from taskhub.models import Worker, Position, Team, Project, Task, TaskType, Commentary


class RegistrationForm(UserCreationForm):
    position = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "Оберіть або введіть нову посаду"
        })
    )

    class Meta:
        model = Worker
        fields = ["username", "email", "position", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input", "placeholder": "Ім'я користувача"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input", "placeholder": "Електронна пошта"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-input", "placeholder": "Пароль"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-input", "placeholder": "Підтвердження паролю"
            }),
        }

    def clean_position(self):
        # Перевіряємо, чи існує позиція. Якщо ні, створюємо нову
        position_name = self.cleaned_data["position"]
        position, created = Position.objects.get_or_create(name=position_name)
        return position


class CreateTeamForm(forms.ModelForm):
    member_ids = forms.CharField(
        label="Member IDs",
        help_text="Enter user IDs separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "e.g., 1, 2, 3"})
    )

    class Meta:
        model = Team
        fields = ["name", "description", "member_ids"]

    def clean_member_ids(self):
        data = self.cleaned_data["member_ids"]
        ids = [id.strip() for id in data.split(",") if id.strip()]
        if not ids:
            raise forms.ValidationError("Member IDs cannot be empty. Please enter valid IDs.")

        try:
            workers = Worker.objects.filter(pk__in=ids)
            if len(workers) != len(ids):
                raise forms.ValidationError("One or more user IDs are invalid. Please check the IDs.")
            return workers
        except ValueError:
            raise forms.ValidationError("Enter valid integers separated by commas.")

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
        members = self.cleaned_data["member_ids"]
        team.members.set(members)
        return team


class CreateProjectForm(forms.ModelForm):
    team_name = forms.CharField(
        label="Team name",
        widget=forms.TextInput(attrs={"placeholder": "Text team name"})
    )

    class Meta:
        model = Project
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "team_name"
        ]

    def clean_team_name(self):
        team_name = self.cleaned_data.get("team_name")
        if not team_name:
            raise forms.ValidationError("Team name cannot be empty. Please enter a valid name.")
        if not Team.objects.filter(name=team_name).exists():
            raise forms.ValidationError(f"Team with name '{team_name}' does not exist.")
        return team_name

    def save(self, commit=True):
        project = super().save(commit=False)
        team_name = self.cleaned_data["team_name"]
        project.team = Team.objects.get(name=team_name)
        if commit:
            project.save()
        return project


class CreateTasksForm(forms.ModelForm):
    assignees_ids = forms.CharField(
        label="Assignees IDs",
        help_text="Enter user IDs separated by commas",
        widget=forms.TextInput(attrs={"placeholder": "e.g., 1, 2, 3"})
    )

    project_name = forms.CharField(
        label="Project name",
        widget=forms.TextInput(attrs={"placeholder": "Text project name"})
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees_ids",
            "project_name"
        ]

    def clean_assignees_ids(self):
        data_ids = self.cleaned_data.get("assignees_ids")
        ids = [id.strip() for id in data_ids.split(",") if id.strip()]
        if not ids:
            raise forms.ValidationError("Member IDs cannot be empty. Please enter valid IDs.")

        try:
            workers = Worker.objects.filter(pk__in=ids)
            if len(workers) != len(ids):
                raise forms.ValidationError("One or more user IDs are invalid. Please check the IDs.")
            return workers
        except ValueError:
            raise forms.ValidationError("Enter valid integers separated by commas.")

    def clean_project_name(self):
        project_name = self.cleaned_data.get("project_name")
        if not project_name:
            raise forms.ValidationError("Project name cannot be empty. Please enter a valid name.")
        try:
            project = Project.objects.get(name=project_name)
            return project
        except Project.DoesNotExist:
            raise forms.ValidationError(f"Project with name '{project_name}' does not exist.")

    def save(self, commit=True):
        task = super().save(commit=False)

        assignees = self.cleaned_data.get("assignees_ids")
        project = self.cleaned_data.get("project_name")

        task.project = project

        if commit:
            task.save()
            task.assignees.set(assignees)
        return task


class CreateCommentaryForm(forms.ModelForm):
    class Meta:
        model = Commentary
        fields = ["commentary_content"]


class AddMemberForm(forms.ModelForm):
    worker_id = forms.IntegerField(
        label="ID працівника",
        required=True
    )

    class Meta:
        model = Worker
        fields = ["worker_id"]

    def clean_worker_id(self):
        worker_id = self.cleaned_data.get("worker_id")
        if not worker_id:
            raise forms.ValidationError("Worker ID cannot be empty. Please enter a valid ID.")
        if not Worker.objects.filter(id=worker_id).exists():
            raise forms.ValidationError(f"Worker with ID '{worker_id}' does not exist.")
        return worker_id
