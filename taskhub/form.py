from django import forms
from django.contrib.auth.forms import UserCreationForm
from taskhub.models import Worker, Position


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
