# Generated by Django 4.0.1 on 2022-03-02 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_posts_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='posts',
            name='total_likes',
            field=models.IntegerField(default=0),
        ),
    ]
