# Generated by Django 4.1.6 on 2023-02-06 19:38

import Forum.models
import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import functools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50, validators=[functools.partial(Forum.models.minimum_length_validator, *(), **{'minimum': 5})])),
            ],
            options={
                'ordering': ['header'],
            },
        ),
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('real_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50, validators=[functools.partial(Forum.models.minimum_length_validator, *(), **{'minimum': 5})])),
                ('text', ckeditor.fields.RichTextField(max_length=32767, validators=[functools.partial(Forum.models.minimum_length_validator, *(), **{'minimum': 50})])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='Forum.forumuser')),
                ('disliked', models.ManyToManyField(related_name='disliked_posts', to='Forum.forumuser')),
                ('liked', models.ManyToManyField(related_name='liked_posts', to='Forum.forumuser')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='Forum.category')),
            ],
            options={
                'ordering': ['date_changed', 'header'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=50, validators=[functools.partial(Forum.models.minimum_length_validator, *(), **{'minimum': 5})])),
                ('text', ckeditor.fields.RichTextField(max_length=32767, validators=[functools.partial(Forum.models.minimum_length_validator, *(), **{'minimum': 50})])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='Forum.forumuser')),
                ('disliked', models.ManyToManyField(related_name='disliked_comments', to='Forum.forumuser')),
                ('liked', models.ManyToManyField(related_name='liked_comments', to='Forum.forumuser')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Forum.post')),
            ],
            options={
                'ordering': ['date_created', 'header'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='last_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Forum.forumuser'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='Forum.category'),
        ),
    ]
