# Generated by Django 5.0.7 on 2024-07-17 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_city_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('name_en', 'name_ru', 'country_code'), 'verbose_name': 'Город', 'verbose_name_plural': 'Города'},
        ),
    ]