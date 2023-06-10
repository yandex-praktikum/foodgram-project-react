from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import UserViewSet

app_name = 'api'
router = SimpleRouter()

router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
