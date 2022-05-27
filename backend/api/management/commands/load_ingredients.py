import json

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = 'Команда для загрузки ингредиентов в базу'

    def handle(self, *args, **options):
        with open(
            'data/ingredients.json',
            encoding='utf-8'
        ) as file:
            ingredients = json.load(file)
        for ingredient in ingredients:
            Ingredient.objects.create(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit']
            )
