from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.serializers import UserSerializers

from .models import (AmountIngredient, Favorite, Follow, Ingredient, Recipe,
                     ShoppingList, Tag)

User = get_user_model()


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
    """ -- Количество ингредиентов для (get) рецепта --"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializers(serializers.ModelSerializer):
    """ -- Список Рецептов -- """

    author = UserSerializers(read_only=True)
    ingredients = AmountIngredientSerializers(
        source='amountingredient',
        many=True
    )
    tags = TagSerializers(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context["request"].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(
                user=user,
                recipe=recipe
            ).exists()
        return False


class ProductSerializer(serializers.ModelSerializer):
    """ -- для создания рецепта -- """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), validators=[
            UniqueValidator(queryset=Ingredient.objects.all())
        ]
    )
    amount = serializers.IntegerField(min_value=0)

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ -- Создание рецепта --"""

    ingredients = ProductSerializer(many=True)
    author = UserSerializers(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def add_ingredients(self, ingredients_data, recipe):
        for ingredient in ingredients_data:
            AmountIngredient.objects.create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['id']
            )

    def add_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        tag_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(image=image_data, **validated_data)
        self.add_tags(tag_data, recipe)
        self.add_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        AmountIngredient.objects.filter(recipe=instance).delete()
        self.add_tags(validated_data.pop('tags'), instance)
        self.add_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)


class PartRecipeSerializers(serializers.ModelSerializer):
    """ -- Рецепт для FollowSerializer -- """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """ Подписка на автора """

    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    recipes = PartRecipeSerializers(many=True)

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
        return follow.recipes.count()
