# Generated by Django 4.2.11 on 2024-05-03 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Satellite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='satellites', to='satapp.owner')),
            ],
        ),
        migrations.CreateModel(
            name='Launcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('launcher_type', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('satellite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='satapp.satellite')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('satellite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='components', to='satapp.satellite')),
            ],
        ),
    ]
