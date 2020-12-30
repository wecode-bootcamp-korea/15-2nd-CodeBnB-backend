# Generated by Django 3.1.4 on 2020-12-30 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0001_initial'),
        ('homes', '0002_auto_20201230_1050'),
        ('users', '0002_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmark_users', through='bookmarks.BookMark', to='homes.Home'),
        ),
    ]