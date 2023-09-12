from django.conf import settings
from django.http.request import HttpRequest


def themes_available_constant(request: HttpRequest):
    return {'THEMES_AVAILABLE': [*settings.THEMES_AVAILABLE.keys()]}
