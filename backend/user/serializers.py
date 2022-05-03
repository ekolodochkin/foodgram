from django.contrib.auth import get_user_model
from rest_framework import serializers, validators


User = get_user_model()


class AccountCreateSerializers(serializers.ModelSerializer):
    """ Создание аккаунта """

    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username'),
                message="Логин и email должны быть уникальными"
            )
        ]


# class SubscribeSerializers(serializers.ModelSerializer):


#     class Meta:
#         model = User
        