# Generated by Django 5.1 on 2024-08-27 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0012_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_type',
            field=models.CharField(choices=[('conference_room', 'Conference Room'), ('meeting_table', 'Meeting Table')], max_length=50),
        ),
    ]
