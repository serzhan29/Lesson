from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    """Упрощённая форма регистрации"""

    error_messages = {
        'password_mismatch': _("Құпия сөздер сәйкес келмейді."),
    }

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']
        labels = {
            'username': 'Пайдаланушы аты:',
            'phone_number': 'Телефон нөмірі:',
            'password1': 'Құпия сөз:',
            'password2': 'Құпия сөзді растау:'
        }
        help_texts = {
            'username': '150 таңбадан артық емес. Әріптер, сандар және @/./+/-/_ рұқсат етілген.',
            'password1': 'Құпия сөз кемінде 8 таңбадан тұруы тиіс және жай ғана сандардан тұрмауы керек.',
            'password2': 'Құпия сөзді қайтадан жазыңыз.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, help_text in self.Meta.help_texts.items():
            if field_name in self.fields:
                self.fields[field_name].help_text = help_text

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Бұл пайдаланушы тіркелген.")
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Бұл телефон нөмір тіркелген.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', self.error_messages['password_mismatch'])
        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_("Пайдаланушы аты"))
    password = forms.CharField(label=_("Құпия сөз"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _(
            "Пайдаланушы аты немесе құпия сөз дұрыс емес. Қайтадан тексеріп көріңіз. "
            "Екеуі де регистрге сезімтал болуы мүмкін."
        ),
        'inactive': _("Бұл аккаунт белсенді емес."),
    }


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
