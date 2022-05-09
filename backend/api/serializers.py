from rest_framework import serializers
from .models import Tag, Recipe, ShoppingList, Ingredient, Favorite, AmountIngredient
from user.serializers import UserSerializers
import base64
from rest_framework.validators import UniqueTogetherValidator

from django.core.files.base import ContentFile


class TagSerializers(serializers.ModelSerializer):
    """ -- Теги -- """

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):
    """ -- Ингредиенты -- """

    class Meta:
        model = Ingredient
        fields = '__all__'


class AmountIngredientSerializers(serializers.ModelSerializer):
    """ -- Количество ингредиентов --"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=AmountIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class Base64Serializers(serializers.ImageField):
    """ -- Кодировка картинки --"""

    def from_native(self, data):
        if isinstance(data, basestring) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super(Base64Serializers, self).from_native(data)


class RecipeSerializers(serializers.ModelSerializer):
    """ -- Список Рецептов -- """

    author = UserSerializers(read_only=True)
    ingredients = AmountIngredientSerializers(source='amountingredient_set', read_only=True, many=True)
    tags = TagSerializers(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64Serializers()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=recipe).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context["request"].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(user=user, recipe=recipe).exists()
        return False


# class RecipeCreateSerializer(serializers.ModelSerializer):