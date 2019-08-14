# Generated by Django 2.2 on 2019-07-29 18:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0008_auto_20190723_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseñaproducto',
            name='calificacion',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Calificación'),
        ),
        migrations.AlterField(
            model_name='reseñaproductor',
            name='calificacion',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Calificación'),
        ),
    ]
