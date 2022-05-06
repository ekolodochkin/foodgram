from rest_framework.response import Response
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import UserRegSerializers, UserSerializers
from api.pagination import MyPagination
from djoser.serializers import SetPasswordSerializer
from .permissions import ForAuthUserOrAllowAny


class CreateRetrieveListViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class UserViewSet(CreateRetrieveListViewSet):
    '''
    View для регистрации, вывода пользователей.
    Добавлены поинты me, set_password.
    Добавлен get_serializer_class для исп.разных сериализаторов
    '''

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializers
    pagination_class = MyPagination
    permission_classes = [ForAuthUserOrAllowAny]
    serializers = {
        'create': UserRegSerializers,
        'me': UserSerializers,
        'set_password': SetPasswordSerializer,
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
