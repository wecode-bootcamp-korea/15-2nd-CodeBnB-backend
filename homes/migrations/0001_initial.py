# Generated by Django 3.1.4 on 2021-01-06 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'beds',
            },
        ),
        migrations.CreateModel(
            name='BuildingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'building_types',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('icon_url', models.URLField(null=True)),
            ],
            options={
                'db_table': 'facilities',
            },
        ),
        migrations.CreateModel(
            name='FacilityType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'facility_types',
            },
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('capacity_guest', models.IntegerField(default=1)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=64)),
                ('latitude', models.DecimalField(decimal_places=6, default=127.0313, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, default=37.30225, max_digits=9)),
            ],
            options={
                'db_table': 'homes',
            },
        ),
        migrations.CreateModel(
            name='HomeFacility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'home_facilities',
            },
        ),
        migrations.CreateModel(
            name='HomeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
            options={
                'db_table': 'home_images',
            },
        ),
        migrations.CreateModel(
            name='HomeOpiton',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'homes_options',
            },
        ),
        migrations.CreateModel(
            name='HomePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
            ],
            options={
                'db_table': 'homes_prices',
            },
        ),
        migrations.CreateModel(
            name='HomeRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'homes_rooms',
            },
        ),
        migrations.CreateModel(
            name='HomeRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.TimeField(null=True)),
                ('check_out', models.TimeField(null=True)),
                ('description', models.CharField(max_length=128, null=True)),
            ],
            options={
                'db_table': 'homes_rules',
            },
        ),
        migrations.CreateModel(
            name='HomeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'home_types',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'options',
            },
        ),
        migrations.CreateModel(
            name='PriceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'price_categories',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('latitude', models.DecimalField(decimal_places=6, default=127.0313, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, default=37.30225, max_digits=9)),
                ('zoom_level', models.IntegerField(default=13)),
                ('around_radius_m', models.IntegerField()),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='RuleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'rule_types',
            },
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('rule_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homes.ruletype')),
            ],
            options={
                'db_table': 'rules',
            },
        ),
        migrations.CreateModel(
            name='RoomBed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('bed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homes.bed')),
                ('home_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homes.homeroom')),
            ],
            options={
                'db_table': 'rooms_beds',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contents', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('rating', models.IntegerField(default=1)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homes.home')),
            ],
            options={
                'db_table': 'reviews',
            },
        ),
    ]
