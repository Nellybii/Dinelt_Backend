# Generated by Django 5.1 on 2024-08-27 06:11

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0010_cart_cartitem_cart_cart_items_order_orderitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='cart_items',
        ),
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 27, 6, 11, 1, 803824, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='foodie_app.cart'),
        ),
    ]
