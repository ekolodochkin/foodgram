import json

from api.models import Ingredient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Команда для загрузки ингредиентов в базу'

    def handle(self, *args, **options):
        with open('D:/Dev/foodgram-project-react/data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.load(file)
        for ingredient in ingredients:
            Ingredient.objects.create(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit']
            )
