from api.pagination import MyPagination
from djoser.serializers import SetPasswordSerializer
from rest_framework import mixins, permissions, status, viewsets, views
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import FollowSerializer
from .models import CustomUser
from .serializers import UserRegSerializers, UserSerializers


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateRetrieveListViewSet):
    """
    View для регистрации, вывода пользователей.
    Добавлены поинты me, set_password, subscriptions
    Добавлен get_serializer_class для исп.разных сериализаторов
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    pagination_class = MyPagination
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
        permission_classes=[permissions.IsAuthenticated],
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
        subscribe_users = CustomUser.objects.filter(follower__author=request.user)
        serializer = self.get_serializer(subscribe_users, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class SubscribeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post()