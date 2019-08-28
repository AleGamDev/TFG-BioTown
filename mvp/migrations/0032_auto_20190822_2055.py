# Generated by Django 2.2 on 2019-08-22 20:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0031_auto_20190819_1903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='total',
            new_name='precioTotal',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='consumidor',
        ),
        migrations.AddField(
            model_name='pago',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PedidoAProductor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Total')),
                ('carrito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.Carrito')),
                ('consumidor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.Consumidor')),
                ('itemCarrito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.ItemCarrito')),
                ('pedido', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.Pedido')),
                ('productor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mvp.Productor')),
            ],
        ),
    ]
