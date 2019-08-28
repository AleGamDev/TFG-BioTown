# Generated by Django 2.2 on 2019-08-16 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0024_itemcarrito_preciototal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='detallesPedido',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='lineaEnvio',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='telefono',
        ),
        migrations.AddField(
            model_name='pedido',
            name='carrito',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='carritoPedido', to='mvp.Carrito'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='consumidor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pedidosConsumidor', to='mvp.Consumidor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('EnProceso', 'En proceso'), ('Terminado', 'Terminado'), ('Cancelado', 'Cancelado')], default='EnProceso', max_length=20, verbose_name='Estado del pedido'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='numeroPedido',
            field=models.CharField(default='ABC', max_length=25, unique=True),
        ),
        migrations.DeleteModel(
            name='LineaEnvio',
        ),
    ]
