# Generated by Django 5.2.1 on 2025-05-30 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BedType',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=10)),
                ('desc', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Dining',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('item_no', models.IntegerField()),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Highlights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image_url', models.URLField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Pizza', 'Pizza'), ('Beverages', 'Beverages'), ('South Indian', 'South Indian'), ('Starters', 'Starters'), ('Dessert', 'Dessert'), ('North Indian', 'North Indian')], default='Beverages', max_length=50)),
                ('description', models.TextField()),
                ('image_url', models.URLField(max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('image_url', models.URLField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Accommodation',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False, unique=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('bed_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydine.bedtype')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='staydine.roomtype')),
            ],
        ),
    ]
