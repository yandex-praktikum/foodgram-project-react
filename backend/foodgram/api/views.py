from django.shortcuts import render, HttpResponse
from djoser.views import UserViewSet
from rest_framework.viewsets import ModelViewSet


from recipes.models import Tag, Recipe
from api.serializers import TagSerializer, RecipeSerializer, RecipeCreateSerializer


def index(request):
    return HttpResponse('YES, I DO')


class CustomUserViewSet(UserViewSet):
    pass


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def dispatch(self, request, *args, **kwargs):
        print(request)
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print(len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])

        return res
    
    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
          'recipe_ingredients__ingredient', 'tags'  
        ).all()
        return recipes
    
    def get_serializer_class(self):
        if self.action == 'create':  # добавить обновление
            return RecipeCreateSerializer
        return RecipeSerializer
    
    def perform_create(self, serializer):
        self.author=self.request.user
        serializer.save(author=self.request.user)


    
