# Generated by Django 5.0.7 on 2024-07-18 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_city_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='city',
            name='region',
            field=models.CharField(max_length=255, verbose_name='Регион'),
        ),
        migrations.AlterField(
            model_name='city',
            name='timezone',
            field=models.CharField(max_length=50, verbose_name='Часовой пояс'),
        ),
        migrations.AlterField(
            model_name='city',
            name='type_of_region',
            field=models.CharField(max_length=8, verbose_name='Тип региона'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'region', 'latitude', 'longitude')},
        ),
    ]