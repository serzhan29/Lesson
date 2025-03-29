from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя"""

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']
        labels = {
            'username': 'Пайдаланушы аты:',
            'middle_name': 'Әкесінің аты:',
            'phone_number': 'Телефон нөмірі:',
            'password1': 'Құпия сөз:',
            'password2': 'Құпия сөзді растау:'
        }
        help_texts = {
            'username': 'Міндетті. 150 таңбадан артық емес. Тек әріптер, сандар және @/./+/-/_. рұқсат етілген.',
            'password1': 'Құпия сөзде кем дегенде 8 таңба болуы керек және тек сандардан тұрмауы тиіс.',
            'password2': 'Тексеру үшін жоғарыдағы құпия сөзді енгізіңіз.'
        }
        error_messages = {
            'password_mismatch': 'Құпия сөздер сәйкес келмейді.',
            'password1': {
                'too_similar': 'Құпия сөз сіздің басқа жеке деректеріңізге тым ұқсас болмауы керек.',
                'password_too_short': 'Құпия сөз кем дегенде 8 таңбадан тұруы тиіс.',
                'password_too_common': 'Бұл құпия сөз тым көп қолданылатын құпия сөз.',
                'password_entirely_numeric': 'Құпия сөз толығымен сандардан тұрмауы керек.'
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = self.Meta.help_texts['username']
        self.fields['password1'].help_text = self.Meta.help_texts['password1']
        self.fields['password2'].help_text = self.Meta.help_texts['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.middle_name = self.cleaned_data.get("middle_name")
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):
    """Форма редактирования профиля пользователя"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'middle_name', 'phone_number', 'birth_date', 'photo']
        labels = {
            'username': 'Пайдаланушы аты:',
            'email': 'Электрондық пошта:',
            'first_name': 'Аты:',
            'last_name': 'Тегі:',
            'middle_name': 'Әкесінің аты:',
            'phone_number': 'Телефон нөмірі:',
            'birth_date': 'Туған күн:',
            'photo': 'Фото:'
        }
