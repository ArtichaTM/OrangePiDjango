from functools import partial

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from ckeditor.fields import RichTextField

from .functions import created_time_delta


__all__ = (
    'Post',
    'Comment'
)


def minimum_length_validator(string: str, /, minimum: int):
    if len(string) < minimum:
        raise ValidationError(
            'Comment should contain at least  %(minimum)s' % {'minimum': minimum}
        )


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='posts_post_comments', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments', null=False)
    text = models.TextField(validators=[partial(minimum_length_validator, minimum=10)], max_length=32767, null=True)
    likes = models.IntegerField(default=0, null=False)
    parent = models.ForeignKey('self', related_name='subcomments', on_delete=models.PROTECT, null=True)
    deleted = models.BooleanField(null=False, default=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    date_changed = models.DateTimeField(auto_now=True, null=False)
    date_deleted = models.DateTimeField(null=True, blank=True)

    def ban_comment(self) -> None:
        self.deleted = True
        self.date_deleted = now()

    def time_passed_since_creation(self) -> str:
        return created_time_delta(self.date_created)

    def __repr__(self) -> str:
        return f"{self.author.username}: {self.text[:20]}"

    def __str__(self) -> str:
        return repr(self)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='posts_posts')
    header = models.CharField(max_length=60, validators=[partial(minimum_length_validator, minimum=7)])
    text = RichTextField(validators=[partial(minimum_length_validator, minimum=50)], max_length=32767)
    text_shortening_index = models.PositiveSmallIntegerField(null=False)

    date_created = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    date_changed = models.DateTimeField(auto_now=True, null=False)

    SHORTENING_MAX_CHARS = 1000

    def _find_shortening_index(self) -> int:

        new_line_index = 0
        for i in range(0, 4):
            new_line_index = self.text.find('\n', new_line_index + 1)

            # Exceeds amount?
            if new_line_index > self.SHORTENING_MAX_CHARS:

                # Checking max as current
                new_line_index = self.SHORTENING_MAX_CHARS

                # Finding convenient end
                new_line_index = self.text.find('</p>', new_line_index)

                # Short enough?
                if new_line_index / self.SHORTENING_MAX_CHARS <= 2:

                    # Return amount
                    return new_line_index

                # Yeah, long enough
                # Simply cut and add "..." to the end
                return self.SHORTENING_MAX_CHARS

        return new_line_index

    def _update_shortening_index(self) -> None:
        self.text_shortening_index = self._find_shortening_index()

    def short_text(self) -> str:
        shortening_index = int(self.text_shortening_index)

        if shortening_index == self.SHORTENING_MAX_CHARS:
            return self.text[:self.SHORTENING_MAX_CHARS] + '\n\n...'

        return self.text[:self.text_shortening_index]

    def time_passed_since_creation(self) -> str:
        return created_time_delta(self.date_created)

    def save(self, *args, **kwargs):
        self._update_shortening_index()
        super().save(*args, **kwargs)

    def __repr__(self) -> str:
        return str(self.header)

    def __str__(self) -> str:
        return repr(self)
