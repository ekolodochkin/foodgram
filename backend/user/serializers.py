from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from api.models import Follow, Recipe
from api.serializers import Base64Serializers

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


class RecipeForFollowSerializer(serializers.ModelSerializer):
    """ -- Рецепт для FollowSerializer -- """

    image = Base64Serializers()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """ Подписка """

    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = RecipeForFollowSerializer(many=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed', 'recipes',
                            'recipes_count')

    def get_is_subscribed(self, follow):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                author=user,
                user=follow
            ).exists()
        return False

    def get_recipes_count(self, follow):
        return Recipe.objects.filter(author=follow.author).count()
