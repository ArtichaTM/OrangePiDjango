from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, Http404
from django.utils.translation import gettext as _
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from .forms import UserLoginForm
from .forms import UserSigninForm

User = get_user_model()


def index(request):
    """ / """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('AuthApp:auth'))
    return render(request, 'AuthApp/index.html')


def auth(request, forms: dict = None):
    context = {
        'LogForm': UserLoginForm(),
        'SignForm': UserSigninForm()
    }

    if forms is not None:
        context.update(forms)

    return render(request, 'AuthApp/auth.html', forms)


def login_view(request):
    if request.method != 'POST':
        HttpResponseRedirect(reverse('AuthApp:auth'))

    form = UserLoginForm(data=request.POST)
    if not form.is_valid():
        return auth(request, {'LogForm': form})

    login(request, form.get_user())

    return HttpResponseRedirect(reverse('AuthApp:index'))


def signin_view(request):
    if request.method != 'POST':
        HttpResponseRedirect(reverse('AuthApp:auth'))

    form = UserSigninForm(request.POST)
    if not form.is_valid():
        return auth(request, {'SignForm': form})

    form.save()

    # Disabling account
    user = User.objects.get(username=form.cleaned_data['username'])
    assert isinstance(user, User)
    user.is_active = False
    user.save()

    form.add_error(None, ValidationError(_('Account created. Wait for activation by administrator')))
    return auth(request, {'SignForm': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('AuthApp:index'))


@login_required
def profile_id(request, target_user: int):
    target_user = get_object_or_404(User, id=target_user)
    return render(request, 'AuthApp/profile.html', {'target_user': target_user})


@login_required
def profile_username(request, target_user: str):
    target_user = get_object_or_404(User, username=target_user)
    return render(request, 'AuthApp/profile.html', {'target_user': target_user})


def change_language(request, target_lang: str):

    language_codes = (lang_tuple[0] for lang_tuple in settings.LANGUAGES)

    if target_lang not in language_codes:
        raise Http404(_("Can't find target language"))

    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, target_lang)

    return response


def change_theme(request, target_theme: str = None):
    if target_theme is None:
        target_theme = settings.THEMES_DEFAULT_THEME
    elif target_theme not in settings.THEMES_AVAILABLE:
        raise Http404(_("Can't find target theme"))

    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.THEMES_COOKIE_NAME, settings.THEMES_AVAILABLE[target_theme])

    return response
