# Generated by Django 3.2.6 on 2021-08-05 14:13

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, unique=True), size=None)),
                ('description', models.TextField()),
            ],
        ),
    ]
