from django import forms
from django.contrib.auth.forms import UserCreationForm
from taskhub.models import Worker, Position, Team, Project


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
