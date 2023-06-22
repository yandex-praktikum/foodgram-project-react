from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, mixins, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.decorators import action, api_view, permission_classes

from .filters import RecipesFilter
from .pagination import OnDemandResultsPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientsSerializer, RecipesGetSerializer,
                          RecipesPostSerializer, TagsSerializer,
                          UserCreateSerializer, UserGetSerializer)
from recipes.models import Ingredients, Recipes, Tags

User = get_user_model()


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    pagination_class = OnDemandResultsPagination

    @action(
        methods=(SAFE_METHODS),
        detail=False,
        permission_classes=(IsAuthenticated,),
        # serializer_class=UserGetSerializer,
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):

        if self.request.method == 'POST':
            return UserCreateSerializer

        return self.serializer_class

    def get_view_name(self):
        return 'Пользователи'


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter,)
    # Поиск по частичному вхождению в начале названия ингредиента.
    search_fields = ('^name',)
    pagination_class = None

    def get_view_name(self):
        return 'Ингредиенты'


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None

    def get_view_name(self):
        return 'Тэги'


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all().select_related()
    serializer_class = RecipesGetSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = OnDemandResultsPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter

    def get_serializer_class(self):

        if self.request.method == 'GET':
            return RecipesGetSerializer
        else:
            return RecipesPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_view_name(self):
        return 'Рецепты'
