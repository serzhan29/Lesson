from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lesson
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','phone_number', 'password1', 'password2']
        labels = {
            'username': 'Пайдаланушы аты:',
            'phone_number': 'Телефон нөмірі',
            'password1': 'Құпия сөз:',
            'password2': 'Құпия сөзді растау:'
        }
        help_texts = {
            'username': 'Міндетті. 150 таңбадан артық емес. Тек әріптер, сандар және@/./+/-/_.',
            'password1': (
                'Құпия сөзде кем дегенде 8 таңба болуы керек. '
                'Құпия сөз тек сандардан тұрмауы керек.'
            ),
            'password2': 'Тексеру үшін жоғарыдағы құпия сөзді енгізіңіз.'
        }


