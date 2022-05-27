from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from api.serializers import (IngredientSerializers, PartRecipeSerializers,
                             RecipeCreateSerializer, RecipeSerializers,
                             TagSerializers)

from .filters import IngredientFilter, RecipeFilters
from .models import (AmountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingList, Tag)
from .pagination import Pagination
from .permissions import IsAuthOwnerOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filterset_class = IngredientFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = Pagination
    permission_classes = [IsAuthOwnerOrReadOnly]
    filterset_class = RecipeFilters

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializers
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = AmountIngredient.objects.filter(
            recipe__shoppinglist__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_total=Sum('amount'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="ShoppingList.pdf"')
        pdf = canvas.Canvas(response)
        pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))
        pdf.setTitle('Список покупок')
        pdf.setFont('Verdana', size=22)
        pdf.drawString(200, 770, 'Список покупок:')
        pdf.setFont('Verdana', size=16)
        height = 670
        for ing in ingredients:
            pdf.drawString(
                50,
                height,
                (
                    f"{ing['ingredient__name']} - "
                    f"{ing['ingredient_total']} "
                    f"{ing['ingredient__measurement_unit']}"
                )
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
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.post_object(ShoppingList, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_object(ShoppingList, request.user, pk)
        return None

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.post_object(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_object(Favorite, request.user, pk)
        return None

    def post_object(self, model, user, pk):
        if model.objects.filter(user=user, recipe_id=pk).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = PartRecipeSerializers(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'},
            status=status.HTTP_400_BAD_REQUEST
        )
