from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, IngredientViewSet, RecipeViewSet


router = DefaultRouter()
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('', include(router.urls)),
]


# Рецепты (get post patch del)
# http://localhost/api/recipes/
# http://localhost/api/recipes/{id}/
#
#
#
#
# Список покупок(get post del)
# http://localhost/api/recipes/download_shopping_cart/
# http://localhost/api/recipes/{id}/shopping_cart/
#
#
#
#
# Избранное (post del)
# http://localhost/api/recipes/{id}/favorite/

#
#
# Ингредиенты (get)
# http://localhost/api/ingredients/
# http://localhost/api/ingredients/{id}/
#