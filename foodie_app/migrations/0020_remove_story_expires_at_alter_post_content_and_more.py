# Generated by Django 5.1 on 2024-08-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodie_app', '0019_alter_menuitem_image_alter_post_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='expires_at',
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='profile_posts', to='foodie_app.post'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='stories',
            field=models.ManyToManyField(blank=True, related_name='profile_stories', to='foodie_app.story'),
        ),
        migrations.AlterField(
            model_name='story',
            name='content',
            field=models.TextField(),
        ),
    ]
