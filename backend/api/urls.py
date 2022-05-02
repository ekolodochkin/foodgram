from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('recipes', )
router.register('tags', )
router.register('ingredients', )


urlpatterns = [
    path('', include(router.urls)),
]


# Рецепты (get post patch del)
# http://localhost/api/recipes/
# http://localhost/api/recipes/{id}/
#
#
#
#Теги (get)
# http://localhost/api/tags/
# http://localhost/api/tags/{id}/
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