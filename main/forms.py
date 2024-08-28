from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lesson

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя:',
            'password1': 'Пароль:',
            'password2': 'Подтверждение пароля:'
        }
        help_texts = {
            'username': 'Обязательно. Не более 150 символов. Только буквы, цифры и @/./+/-/_.',
            'password1': (
                'Ваш пароль не должен быть слишком похож на другую личную информацию. '
                'Пароль должен содержать как минимум 8 символов. '
                'Пароль не должен состоять только из цифр.'
            ),
            'password2': 'Введите тот же пароль, что и выше, для проверки.'
        }


