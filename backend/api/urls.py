from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, TagViewSet

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
