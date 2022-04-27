from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    ''' -- Теги - теги на выбор из определенных цвецов в формате HEX -- '''

    RED = 'ff0000'
    BLUE = '0037ff'
    GREEN = '37ff00'
    YELLOW = 'fffb00'
    PURPLE = 'e600ff'

    COLOR_CHOISE = [
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
        choices=COLOR_CHOISE
    )
    slug = models.SlugField('Слаг', unique=True, max_length=50)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ''' -- Ингредиенты -- '''

    name = models.CharField('Ингредиент', max_length=200)
    amount = models.IntegerField(models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(1, 'Минимальное количество 1')]
        )
    )
    measurement_unit = models.CharField('Ед.измерения веса', max_length=3)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ''' -- Рецепт -- '''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название рецепта', max_length=200)
    image = models.ImageField('Фото', upload_to='image_recipes/')
    text = models.TextField('Описание', max_length=1000)
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
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


class Favorite(models.Model):
    ''' -- Избранное -- '''

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f' {self.user} добавил в избранное {self.recipe}'


class Follow(models.Model):
    ''' -- Подписка -- '''

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_follow_user"
            )
        ]

    def __str__(self):
        return f' на {self.author} подписался {self.user}'


class ShoppingList(models.Model):
    ''' -- Список покупок --'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='shoppinglist',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppinglist',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_user'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в список покупок {self.recipe}'
