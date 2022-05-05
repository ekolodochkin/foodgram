from rest_framework import serializers
from .models import Tag, Recipe, ShoppingList, Ingredient, Favorite, AmountIngredient


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class AmountIngredientSerializers(serializers.ModelSerializer):
    


class RecipeSerializers(serializers.ModelSerializer):



class RecipeCreateSerializer(serializers.ModelSerializer):