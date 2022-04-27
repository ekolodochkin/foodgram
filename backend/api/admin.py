from django.contrib import admin
from .models import Tag, Recipe, Ingredient, Favorite, Follow, ShoppingList


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('__all__')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    search_fields = ('author', 'name', 'tags')
    ordering = ('-id',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(ShoppingList)
