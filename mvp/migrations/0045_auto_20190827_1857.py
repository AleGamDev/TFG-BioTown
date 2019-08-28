# Generated by Django 2.2 on 2019-08-27 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0044_auto_20190827_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pago',
            old_name='precioTotal',
            new_name='precio',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='consumidor',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='fechaHora',
        ),
        migrations.RemoveField(
            model_name='pago',
            name='paypalId',
        ),
        migrations.AddField(
            model_name='pago',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pago',
            name='payer_email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='pago',
            name='payer_id',
            field=models.CharField(blank=True, db_index=True, max_length=128),
        ),
        migrations.AddField(
            model_name='pago',
            name='payment_id',
            field=models.CharField(db_index=True, default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pago',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.Pedido'),
        ),
    ]