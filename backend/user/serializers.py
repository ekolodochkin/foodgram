from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from api.models import Follow


User = get_user_model()


class UserRegSerializers(serializers.ModelSerializer):
    """ -- Регистрация юзера -- """

    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password',)
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

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializers(serializers.ModelSerializer):
    """ -- Юзер + подписчик -- """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password', 'is_subscribed')

    def get_is_subscribed(self, subscribe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                author=user,
                user=subscribe
            ).exists()
        return False

