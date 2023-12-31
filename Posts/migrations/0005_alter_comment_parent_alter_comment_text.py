# Generated by Django 4.1.6 on 2023-02-08 18:16

import Posts.models
from django.db import migrations, models
import django.db.models.deletion
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subcomments', to='Posts.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(max_length=32767, null=True, validators=[functools.partial(Posts.models.minimum_length_validator, *(), **{'minimum': 10})]),
        ),
    ]
