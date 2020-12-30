# Generated by Django 3.1.4 on 2020-12-30 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homes', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=32)),
                ('is_valid', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('commission_date', models.DateTimeField(auto_now_add=True)),
                ('is_superhost', models.BooleanField(default=False)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_host', to='homes.home')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_host', to='users.user')),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
    ]