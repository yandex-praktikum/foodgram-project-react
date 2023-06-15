from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, token

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', token, name='login'),
]
