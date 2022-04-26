from django.contrib import admin
from .models import Tag, Recipe, Ingredient
# Подписки / избранное / список покупок


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('__all__')
    search_fields = ('name,')
    empty_value_display = '-empty-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('author', 'name', 'tags')
    ordering = ('-id',)
    empty_value_display = '-empty-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    empty_value_display = '-empty-'