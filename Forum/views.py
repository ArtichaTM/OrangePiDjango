from django.shortcuts import render
from django.http.response import Http404


def index(request):
    raise Http404()
