from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        "User",
    )
    name = models.CharField('название рецепта', max_length=200)
    image = models.ImageField()
    text = models.TextField('описание')
    ingredients =
    tags =
    cooking_time =

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Teg(models.Model):
    name = models.CharField('тег', max_length=200)
    color =
    slug = models.SlugField('слаг', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('ингредиенты', max_length=200)
    amount = models.IntegerField('количество', )
    measurement_unit = ('ед.измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name