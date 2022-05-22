# Generated by Django 4.0.4 on 2022-05-21 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_amountingredient_ingredient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_amount', to='api.ingredient', verbose_name='Ингридиент'),
        ),
        migrations.AlterField(
            model_name='amountingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_amount', to='api.recipe', verbose_name='Рецепт'),
        ),
    ]
