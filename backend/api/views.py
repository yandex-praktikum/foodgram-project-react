from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import (
    TagSerializer,
)
from recipes.models import (
    Tag,
)
from api.permissions import ReadOnlyPermission

class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnlyPermission,)