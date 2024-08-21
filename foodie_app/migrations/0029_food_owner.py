# Generated by Django 5.1 on 2024-08-21 14:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0028_profile_is_business_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='owner',
            field=models.ForeignKey(default=77, on_delete=django.db.models.deletion.CASCADE, related_name='foods', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
