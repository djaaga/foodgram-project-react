
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_recipeingredient_unique_ingredients_recipes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Рецепт и ингредиент', 'verbose_name_plural': 'Рецепт и ингредиенты'},
        ),
    ]
