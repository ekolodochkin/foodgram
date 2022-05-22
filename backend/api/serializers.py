from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
    """ -- Количество ингредиентов --"""

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
    ingredients = AmountIngredientSerializers(source='recipe_amount', many=True)
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
            return Favorite.objects.filter(user=user, recipe=recipe).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context["request"].user
        if user.is_authenticated:
            return ShoppingList.objects.filter(user=user, recipe=recipe).exists()
        return False

    def create_ingredients(ingredients_data, recipe):
        for ingredient in ingredients_data:
            AmountIngredient.objects.create(
                recipe=recipe,
                amount=ingredients_data.get('amount'),
                ingredient_id=ingredient.get('id')
            )

    def create(self, validated_data):
        print(validated_data)
        image_data = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image_data, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        AmountIngredient.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


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
