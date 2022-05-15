from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Ingredient, Recipe, ShoppingList, Tag, Favorite
from .pagination import MyPagination
from .serializers import (IngredientSerializers, RecipeSerializers,
                          TagSerializers, PartRecipeSerializers)
from django.shortcuts import get_object_or_404

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # @action(
    #     methods=[],
    #     detail=,
    #     permission_classes=[IsAuthenticated],
    # )
    # def download_shopping_cart(self, request):

    @action(
        methods=['GET', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            if ShoppingList.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response(
                    {'Error': 'Рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            serializer = PartRecipeSerializers(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            shoppinglst = ShoppingList.objects.filter(user=request.user, recipe__id=pk)
            if shoppinglst.exists():
                shoppinglst.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт уже удален'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['GET', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'GET':
            if Favorite.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response(
                    {'Error': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=request.user, recipe=recipe)
            serializer = PartRecipeSerializers(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=request.user, recipe__id=pk)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепт уже удален'},
                status=status.HTTP_400_BAD_REQUEST
            )
