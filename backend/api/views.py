from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (IngredientSerializers, PartRecipeSerializers,
                             RecipeSerializers, TagSerializers)

from .models import (AmountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingList, Tag)
from .pagination import MyPagination
from .permissions import IsAuthOwnerOrReadOnly


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
    permission_classes = [IsAuthOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.shoppinglist.all()
        shopping_list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = AmountIngredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                amount = ingredient.amount
                if name not in shopping_list:
                    shopping_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ShoppingList.pdf"'
        pdf = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        pdf.setTitle('Список покупок')
        pdf.setFont('Verdana', size=22)
        pdf.drawString(200, 770, 'Список покупок:')
        pdf.setFont('Verdana', size=16)
        height = 670
        for name, data in shopping_list.items():
            pdf.drawString(
                50,
                height,
                f"{name} ({data['measurement_unit']}) - {data['amount']} "
            )
            height -= 25
        pdf.showPage()
        pdf.save()
        return response


    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            if ShoppingList.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в список покупок'},
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
                {'errors': 'Вы уже удалили этот рецепт'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            if Favorite.objects.filter(user=request.user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'Рецепт уже добавлен в избранное'},
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
                {'errors': 'Вы уже удалили этот рецепт'},
                status=status.HTTP_400_BAD_REQUEST
            )
