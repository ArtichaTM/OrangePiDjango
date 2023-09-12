from functools import partial

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from ckeditor.fields import RichTextField


def minimum_length_validator(string: str, /, minimum: int):
    if len(string) < minimum:
        raise ValidationError(
            'Comment should contain at least  %(minimum)s' % {'minimum': minimum}
        )


class AbstractPost(models.Model):
    header = models.CharField(max_length=50, validators=[partial(minimum_length_validator, minimum=5)], null=False)
    text = RichTextField(validators=[partial(minimum_length_validator, minimum=50)], max_length=32767, null=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    date_changed = models.DateTimeField(auto_now=True, null=False)

    def likes_overall(self):
        return self.liked.all().count() - self.disliked.all().count()

    class Meta:
        abstract = True


class Post(AbstractPost):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='forum_posts')
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, null=False, related_name='posts')

    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forum_liked_posts')
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forum_disliked_posts')

    class Meta:
        ordering = ['date_changed', 'header']


class Comment(AbstractPost):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='forum_comments')
    parent = models.ForeignKey('Post', on_delete=models.CASCADE, null=False, related_name='comments')

    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forum_liked_comments')
    disliked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='forum_disliked_comments')

    class Meta:
        ordering = ['date_created', 'header']


class Category(models.Model):
    header = models.CharField(max_length=50, validators=[partial(minimum_length_validator, minimum=5)], null=False)
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='subcategories')

    last_post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, parent_link=False)

    def check_last_post(self):
        ...

    class Meta:
        ordering = ['header']
