# Generated by Django 4.0.4 on 2022-05-21 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='image_recipes/', verbose_name='Фото'),
        ),
    ]