# Generated by Django 5.1 on 2024-08-12 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0011_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
