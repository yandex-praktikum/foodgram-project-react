from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TagViewset


app_name = 'api'

router = DefaultRouter()
router.register('tags', TagViewset, 'tags')

urlpatterns = [
    path('', include(router.urls)),
]