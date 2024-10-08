# Generated by Django 5.1 on 2024-08-26 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0008_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='food',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_items',
        ),
        migrations.RemoveField(
            model_name='order',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='food',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
