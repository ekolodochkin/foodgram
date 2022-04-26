from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class Teg(models.Model):
    RED = 'ff0000'
    BLUE = '0037ff'
    GREEN = '37ff00'
    YELLOW = 'fffb00'
    PURPLE = 'e600ff'

    color_choise = [
        (RED, 'Красный'),
        (BLUE, 'Синий'),
        (GREEN, 'Зеленый'),
        (YELLOW, 'Желтый'),
        (PURPLE, 'Фиолетовый'),
    ]

    name = models.CharField('Тег', max_length=200)
    color = models.CharField(
        'Цвет в HEX',
        unique=True,
        choices=color_choise
    )
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', max_length=200)
    amount = models.IntegerField('Количество')
    measurement_unit = models.CharField('Ед.измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
        

class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        """related_name=""",
        verbose_name='Автор'
    )
    name = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Фото', )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        """related_name=""",
        verbose_name='Ингредиенты'
    )
    tags =
    cooking_time = models.PositiveIntegerField(
        'Время в минутах',
        validators=[MinValueValidator(1, 'Минимальное время 1 минута')]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


# Разобраться с картинкой
# разобраться с релейт нейм
# разобраться с tags recipe