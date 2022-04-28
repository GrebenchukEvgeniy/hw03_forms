from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User

from .models import Group, Post

from .forms import PostForm


NUM_OF_PUBLICATIONS: int = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUM_OF_PUBLICATIONS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, NUM_OF_PUBLICATIONS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related()
    post_count = posts.count()
    paginator = Paginator(posts, NUM_OF_PUBLICATIONS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = get_object_or_404(User, id=post.author.id)
    full_name = user.get_full_name()
    post_count = user.posts.select_related().count()
    context = {
        'post': post,
        'user': user,
        'full_name': full_name,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
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
    else:
        if request.method != 'POST':
            form = PostForm(instance=post)
        else:
            form = PostForm(instance=post, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('posts:post_detail', post_id=post_id)
        context = {'form': form, 'post': post, 'is_edit': is_edit}
        return render(request, 'posts/create_post.html', context)
