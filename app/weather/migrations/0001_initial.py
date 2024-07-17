# Generated by Django 5.0.7 on 2024-07-17 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=255, verbose_name='Название (en)')),
                ('name_ru', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название (ru)')),
                ('country_code', models.CharField(max_length=255, verbose_name='Код страны')),
                ('latitude', models.FloatField(verbose_name='Широта')),
                ('longitude', models.FloatField(verbose_name='Долгота')),
                ('search_count', models.PositiveBigIntegerField(default=0, verbose_name='Кол-во поисковых запросов')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('name_ru', 'name_en', 'country_code'),
                'unique_together': {('name_en', 'country_code')},
            },
        ),
    ]
