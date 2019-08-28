# Generated by Django 2.2 on 2019-08-28 18:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0049_auto_20190828_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioTotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Total')),
                ('paypalId', models.CharField(max_length=100, null=True)),
                ('fechaHora', models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora')),
                ('consumidor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.Consumidor')),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mvp.Pedido')),
            ],
        ),
        migrations.DeleteModel(
            name='PagoPaypal',
        ),
    ]
