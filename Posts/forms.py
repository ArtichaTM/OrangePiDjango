from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Post, Comment


__all__ = (
    'NewPostForm',
    'EditPostForm',
    'NewCommentForm'
)


class NewPostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['header', 'text']


class EditPostForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['header', 'text']


class NewCommentForm(forms.ModelForm):
    parent = forms.IntegerField(min_value=0, max_value=9223372036854775807, required=False)
    text = forms.Textarea()

    class Meta:
        model = Comment
        fields = ['parent','text']
