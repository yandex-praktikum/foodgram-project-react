from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


class TagsViewSet(ModelViewSet):
    '''Вьювсет для работы с API тегов'''
    pass


class UsersViewSet(ModelViewSet):
    '''Вьювсет для работы с API юзеров'''
    pass


class RecipesViewSet(ModelViewSet):
    '''Вьювсет для работы с API рецептов'''
    pass


class IngridientsViewSet(ModelViewSet):
    '''Вьювсет для работы с API ингридиентов'''
    pass

