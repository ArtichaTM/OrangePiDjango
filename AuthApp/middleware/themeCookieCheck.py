from django.conf import settings
from django.shortcuts import reverse
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.template.base import VariableDoesNotExist


class ThemeCookieCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        return response

    def process_exception(self, _: HttpRequest, exception: Exception):

        # Force default theme, if user didn't select any
        if isinstance(exception, VariableDoesNotExist) and exception.params[0] == settings.THEMES_COOKIE_NAME:
            return HttpResponseRedirect(reverse('AuthApp:change_theme', args=(settings.THEMES_DEFAULT_THEME,)))
