# Generated by Django 4.0.1 on 2022-03-28 10:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_posts_options_posts_total_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='follows',
            field=models.ManyToManyField(related_name='user_follows', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
