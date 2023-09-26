from django.shortcuts import render, HttpResponse
from djoser.views import UserViewSet

def index(request):
    return HttpResponse('YES, I DO')


class CustomUserViewSet(UserViewSet):
    pass

