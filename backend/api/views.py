from rest_framework.response import Response
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializers, IngredientSerializers, RecipeSerializers
from .pagination import MyPagination
# from .permissions import 


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = MyPagination
    serializer_class = RecipeSerializers
