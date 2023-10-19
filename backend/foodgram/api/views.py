from http import HTTPStatus


from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count, Prefetch, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.exceptions import BadRequestException
from api.serializers import (CustomUserSerializer, IngredientsSerializer, RecipesPostSerializer,
                             RecipesSerializer, TagsSerializer, SubscribeSerializer, SubscriptionSerializer)
from api.viewsets import CreateDestroyViewSet, ListViewSet
from recipes.models import (Ingredient,
                            IngredientRecipe, Recipe, Tag, Subscription)

User = get_user_model()



class CustomSerializerContext(generics.GenericAPIView):

    def get_serializer_context(self):
        subscribtions = None
        recipes = None
        if self.request.user.is_authenticated:
            subscribtions = set(Subscription.objects.filter(
                subscriber=self.request.user).values_list(
                    'author_id', flat=True))
            recipes = Recipe.objects.filter(author__in=subscribtions)
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'subscribtions': subscribtions,
            'recipes': recipes
        }



class CustomUserViewSet(UserViewSet, CustomSerializerContext): # 
    pass


class IngridientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.select_related('measurement_unit').all()
    serializer_class = IngredientsSerializer
    # permission_classes = (AllowAny, )
    pagination_class = None
    ordering = ('name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    # permission_classes = (AllowAny, )
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

class SubscriptionsViewSet(ListViewSet, CustomSerializerContext):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            id__in=user.subscriber.values('author_id')).annotate(
                recipes_count=Count('recipes'))


class SubscribeViewSet(CreateDestroyViewSet, CustomSerializerContext):
    serializer_class = SubscribeSerializer
    permission_classes = (IsAuthenticated,)
    ordering = ('author',)

    def dispatch(self, request, *args, **kwargs):
        print(request)
        res = super().dispatch(request, *args, **kwargs)

        from django.db import connection
        print(len(connection.queries))
        for q in connection.queries:
            print('>>>>', q['sql'])

        return res

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        author = get_object_or_404(User, pk=self.kwargs['id'])
        subscriber = self.request.user
        if not Subscription.objects.filter(author=author,
                                           subscriber=subscriber).exists():
            raise BadRequestException(
                {'errors': 'Вы не подписаны на этого автора!'})
        return get_object_or_404(queryset, subscriber=subscriber,
                                 author=author)

    def get_queryset(self):
        user_query = User.objects.all().annotate(
            recipes_count=Count('recipes'))
        return Subscription.objects.select_related(
            'subscriber').prefetch_related(Prefetch('author',
                                                    queryset=user_query))

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.kwargs['id'])
        serializer.save(subscriber=self.request.user, author=author)
   




