from django.contrib import admin
from .models import Tag, Recipe, Ingredient, Favorite, Follow, ShoppingList


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('__all__')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'add_favorite')
    search_fields = ('author', 'name', 'tags')
    ordering = ('-id',)
    
    def add_favorite(self, obj):
        return obj.favorites.count()

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(ShoppingList)
