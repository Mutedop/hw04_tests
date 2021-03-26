from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    latest = Post.objects.all()
    paginator = Paginator(latest, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'group.html',
        {'group': group, 'page': page, 'paginator': paginator}
    )


@login_required
def new_post(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    return render(request, 'new.html', {'form': form})


def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    if request.user != post.author:
        return redirect('post', username=username, post_id=post.id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post.id)
    return render(
        request,
        'new.html',
        {'form': form, 'post': post, 'is_edit': True})


def card_user(request, username):
    post_author = User.objects.get(username=username)
    user_posts = Post.objects.all().filter(author=post_author)
    posts_count = post_author.posts.count()
    context = {
        'author': post_author,
        'post': user_posts,
        'posts_count': posts_count,
    }
    return render(request, 'card_user.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'author': user,
               'page': page,
               'paginator': paginator}
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    user = get_object_or_404(User, username=username)
    post = get_object_or_404(
        Post.objects.select_related('author').filter(id=post_id)
    )
    context = {
        'author': user,
        'post': post,
    }
    return render(request, 'post.html', context)
