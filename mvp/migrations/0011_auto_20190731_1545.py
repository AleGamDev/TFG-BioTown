# Generated by Django 2.2 on 2019-07-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0010_auto_20190731_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reseñaproductor',
            name='calificacion',
            field=models.IntegerField(choices=[(5, '5'), (4, '4'), (3, '3'), (2, '2'), (1, '1')], default=1, verbose_name='Calificación'),
        ),
    ]