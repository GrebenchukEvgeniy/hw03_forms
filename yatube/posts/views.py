from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post
from .utils import my_paginator


def index(request):
    post_list = Post.objects.all()
    page_obj = my_paginator(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = my_paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related()
    page_obj = my_paginator(request, post_list)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related(), id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post_create = form.save(commit=False)
        post_create.author = request.user
        post_create.save()
        return redirect('posts:profile', username=request.user)
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    is_edit = True
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(instance=post, data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {'form': form, 'post': post, 'is_edit': is_edit}
    return render(request, 'posts/create_post.html', context)
