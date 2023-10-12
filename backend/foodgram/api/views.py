from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Count, Prefetch, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated


from api.serializers import (CustomUserSerializer,                         ###
                             IngredientsSerializer, RecipesPostSerializer,
                             RecipesSerializer, TagsSerializer)
from api.viewsets import CreateDestroyViewSet, ListViewSet
from recipes.models import (Ingredient,
                            IngredientRecipe, Recipe, Tag, )

User = get_user_model()

"""
class CustomSerializerContext(generics.GenericAPIView):

    def get_serializer_context(self):
        subscribtions = None
        favorites = None
        shopping_carts = None
        recipes = None
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscribtions': subscribtions,
            'favorites': favorites,
            'shopping_carts': shopping_carts,
            'recipes': recipes
        }
"""


class CustomUserViewSet(UserViewSet): # , CustomSerializerContext
     
    pass


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.select_related('measurement_unit').all()
    serializer_class = IngredientsSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    ordering = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    ordering = ('name',)


class RecipesViewSet(viewsets.ModelViewSet):  # , CustomSerializerContext

    queryset = Recipe.objects.select_related(
        'author').prefetch_related('tags', 'ingredients_recipes').all()
    serializer_class = RecipesSerializer
    ordering = ('-pub_date',)

    """
        def dispatch(self, request, *args, **kwargs):
        print(request)
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print(len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])

        return res
    """

    # def perform_create(self, serializer):
        # serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipesPostSerializer
        return RecipesSerializer
