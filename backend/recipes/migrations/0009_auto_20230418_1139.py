
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_favorites_recipe'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorites',
            options={'ordering': ('-id',), 'verbose_name': 'Избранное', 'verbose_name_plural': 'Избранные'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ('-id',), 'verbose_name': 'Покупка', 'verbose_name_plural': 'Покупки'},
        ),
    ]
