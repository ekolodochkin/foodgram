from rest_framework.response import Response
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from .models import Tag
from .serializers import TagSerializers
from api.pagination import MyPagination
# from .permissions import 


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers