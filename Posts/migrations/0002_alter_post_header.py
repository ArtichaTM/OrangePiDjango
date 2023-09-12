# Generated by Django 4.1.6 on 2023-02-07 23:27

import Posts.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header',
            field=models.CharField(max_length=60, validators=[functools.partial(Posts.models.minimum_length_validator, *(), **{'minimum': 7})]),
        ),
    ]