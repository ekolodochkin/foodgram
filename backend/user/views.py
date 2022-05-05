from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import filters, permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserRegSerializers, UserSerializers
from api.pagination import MyPagination


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = MyPagination
    # permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['username', 'email']

    # @action(detail=False, methods=['get', 'patch'],
    #         permission_classes=[permissions.IsAuthenticated])
    # def me(self, request):
    #     if request.method == 'GET':
    #         serializer = self.get_serializer(request.user)
    #         return Response(data=serializer.data)
    #     if request.method == 'PATCH':
    #         serializer = self.get_serializer(
    #             request.user,
    #             data=request.data,
    #             partial=True
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(role=request.user.role)
    #         return Response(data=serializer.data)
