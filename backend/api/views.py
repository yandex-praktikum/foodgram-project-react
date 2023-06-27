from users.models import User, Subscribe
from djoser.views import UserViewSet
from .serializers import (
    CustomUserSerializer, SubscribeSerializer, TagSerializer,
    IngredientSerilizer, RecipesPostUpdateSerializer, RecipesSerializer
    )
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from recipes.models import Tag, Ingredient, Recipes


class UsersViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ('username', 'email')
    permission_classes = (AllowAny,)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeSerializer(
                Subscribe.objects.create(user=request.user, author=author),
                context={'request': request},
            )
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        Subscribe.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)

    @action(detail=False)
    def get_tag(self, request):
        tag = Tag.objects.all()
        serializer = self.get_serializer(tag, many=True)
        return Response(serializer.data)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerilizer
    permission_classes = (AllowAny,)

    @action(detail=False)
    def get_ingredients(self, request):
        ingredient = Ingredient.objects.all()
        serializer = self.get_serializer(ingredient, many=True)
        return Response(serializer.data)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AllowAny,)

    @action(detail=False, methods=['get'])
    def get_recipes(self, request):
        recipes = Recipes.objects.all()
        serializer = RecipesSerializer(recipes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def post_recipes(self, request):
        serializer = RecipesPostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipesSerializer
        return RecipesPostUpdateSerializer
