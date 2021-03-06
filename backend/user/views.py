from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Follow
from api.pagination import Pagination
from api.serializers import FollowSerializer
from user.mixins import CreateRetrieveListViewSet
from user.models import CustomUser
from user.permissions import AllowAnyGetPost, CurrentUserOrAdmin
from user.serializers import UserRegSerializers, UserSerializers


class UserViewSet(CreateRetrieveListViewSet):
    """
    View для регистрации, вывода пользователей.
    Добавлены поинты me, set_password, subscriptions
    Добавлен get_serializer_class для исп.разных сериализаторов
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    pagination_class = Pagination
    permission_classes = [AllowAnyGetPost]
    serializers = {
        'create': UserRegSerializers,
        'me': UserSerializers,
        'set_password': SetPasswordSerializer,
        'subscriptions': FollowSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializers[self.action]
        except KeyError:
            return self.serializer_class

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=[CurrentUserOrAdmin],
    )
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(
            serializer.validated_data.get('new_password')
        )
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        subscribe_users = CustomUser.objects.filter(
            follower__author=request.user
        )
        serializer = self.get_serializer(subscribe_users, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class SubscribeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        subscribe_user = get_object_or_404(CustomUser, id=user_id)
        double_subscribe = Follow.objects.filter(
            author=request.user,
            user=subscribe_user
        ).exists()
        if request.user.id == int(user_id):
            error = {'errors': 'Невозможно подписаться на самого себя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        elif double_subscribe:
            error = {'errors': 'Вы уже подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(
            author=request.user,
            user=subscribe_user
        )
        serializer = FollowSerializer(
            subscribe_user,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscribe_user = get_object_or_404(CustomUser, id=user_id)
        try:
            subscribe = Follow.objects.get(
                author=request.user,
                user=subscribe_user
            )
        except Follow.DoesNotExist:
            error = {'errors': 'Вы не подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
