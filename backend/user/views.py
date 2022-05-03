from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import AccountCreateSerializers


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountCreateSerializers
    http_method_names = ['get', 'post', 'patch', 'delete']
    # permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ['username']

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(data=serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(data=serializer.data)
