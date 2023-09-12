from string import ascii_letters, digits

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User

    def clean(self):
        try:
            user = User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            raise ValidationError('Пользователь не существует', code='404')

        if not user.is_active:
            raise ValidationError('Аккаунт не активирован. Обратитесь к администратору', code='inactive')
        return super().clean()


class UserSigninForm(UserCreationForm):
    letters_set = set(ascii_letters)
    digits_set = set(digits)

    password2 = None

    PASSWORD_MIN_CHARACTERS = 9
    USERNAME_MIN_CHARACTERS = 5
    PASSWORD_UNIQUE_CHARACTERS = 5

    class Meta:
        model = User
        fields = ['username', 'password1', 'email']

    def clean_password(self) -> bool:
        password = self.cleaned_data['password1']
        if len(password) < self.PASSWORD_MIN_CHARACTERS:

            message = _('Password should contain at least %(amount)s symbols')
            message = message % {'amount': self.PASSWORD_MIN_CHARACTERS}

            raise ValidationError(message)

        password_set = set(password)
        if len(password_set) < self.PASSWORD_UNIQUE_CHARACTERS:

            message = _('Password should contain at least %(amount)s unique symbols')
            message = message % {'amount': self.PASSWORD_UNIQUE_CHARACTERS}

            raise ValidationError(message)

        return self.cleaned_data['password1']

    def clean_username(self) -> bool:
        username = self.cleaned_data['username']
        if len(username) < 5:

            message = _('Username should contain at least %(amount)s symbols')
            message = message % {'amount': self.USERNAME_MIN_CHARACTERS}

            raise ValidationError(message)

        if username[0] not in ascii_letters:
            raise ValidationError(_('Username should start with letter'))

        return self.cleaned_data['username']
