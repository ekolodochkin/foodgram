from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from api.models import Follow


User = get_user_model()


class UserRegSerializers(serializers.ModelSerializer):
    """ Регистрация юзера """

    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())])

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
    """ Юзер + подписчик """

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


# class SubscribeSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()
#     recipes = RecipePartialSerializer(many=True)
#     recipes_count = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name', 'last_name',
#                   'is_subscribed', 'recipes', 'recipes_count')
#         read_only_fields = ('email', 'id', 'username', 'first_name',
#                             'last_name', 'is_subscribed', 'recipes',
#                             'recipes_count')

#     def get_is_subscribed(self, subscribe):
#         user = self.context['request'].user
#         if user.is_authenticated:
#             return Subscription.objects.filter(
#                 user=user,
#                 subscribe=subscribe
#             ).exists()
#         return False

#     def get_recipes_count(self, subscribe):
#         return subscribe.recipes.count()
