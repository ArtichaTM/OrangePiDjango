from django.shortcuts import render, Http404, redirect, get_object_or_404
from django.http.response import HttpResponseForbidden, HttpResponse
from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.urls import reverse

from .models import *
from .forms import *


@login_required
def index(request: HttpRequest):
    posts = Post.objects.order_by('date_created')[:5]
    return render(request, 'Posts/index.html', context={'posts': posts})


@login_required
def new_post(request: HttpRequest, forms: dict = None):
    context = {
        'postForm': NewPostForm(),
    }
    if forms is not None:
        context.update(forms)

    return render(request, 'Posts/post_new.html', context)


@login_required
def add_post(request: HttpRequest):

    # Checking for POST. Otherwise 404
    if request.method != 'POST':
        raise Http404()

    # Creating form from POST data
    form = NewPostForm(data=request.POST)

    # Return new request, if
    if not form.is_valid():
        return new_post(request, {'postForm': form})

    model: Post = form.save(commit=False)
    model.author = request.user
    model.save()

    return redirect(reverse('Posts:view_post', kwargs={'post_id': model.pk}))


@login_required
def view_post(request: HttpRequest, post_id: int):

    # Getting post by id
    post: Post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,
        'newCommentForm': NewCommentForm()
    }

    # Returning response
    return render(request, 'Posts/post.html', context=context)


@login_required
def edit_post(request: HttpRequest, post_id: int, forms: dict = None):

    post: Post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden(_('You have no rights to edit this post'))

    context = {
        'postForm': EditPostForm(),
        'post': post
    }
    if forms is not None:
        context.update(forms)

    return render(request, 'Posts/post_edit.html', context)


@login_required
def update_post(request: HttpRequest, post_id: int):

    post: Post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden(_('You have no rights to edit this post'))

    # Checking for PUT. Otherwise 404
    if request.method != 'POST':
        raise Http404()

    # Creating form from POST data
    form = EditPostForm(data=request.POST)

    # Return new request, if
    if not form.is_valid():
        return edit_post(request, post_id, forms={'postForm': form})

    # Updating post
    post.text = form.cleaned_data['text']
    post.header = form.cleaned_data['header']
    post.save()

    return redirect(reverse('Posts:view_post', kwargs={'post_id': post.id}))


@login_required
def add_comment(request: HttpRequest, post_id: id):

    post: Post = get_object_or_404(Post, id=post_id)

    # Checking for PUT. Otherwise 404
    if request.method != 'POST':
        raise Http404()

    # Creating form from POST data
    form = NewCommentForm(data=request.POST)

    if not form.is_valid():
        context = {'form': form}
        return render(request, 'Posts/subtemplates/new_comment.html', context=context)

    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()

    return HttpResponse(status=201)
