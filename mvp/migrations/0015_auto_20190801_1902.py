# Generated by Django 2.2 on 2019-08-01 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0014_auto_20190801_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='titulo',
            field=models.CharField(max_length=150, verbose_name='Título'),
        ),
    ]
