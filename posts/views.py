from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Post, Group
from .forms import PostForm


User = get_user_model()


def index(request):
    post_list = Post.objects.order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    response = render(request, 'index.html', {'page': page})
    return response


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:12]
    response = render(request, 'group.html',
                      {'group': group, 'posts': posts})
    return response


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.text = form.cleaned_data['text']
        new_post.save()
        return redirect('index')
    return render(request, 'new_post.html', {'form': form})


def profile(request, username):
    if request.method == 'GET':
        user = request.user
        author = User.objects.get(username=username)
        post_list = Post.objects.filter(author_id=author.id).order_by('-pub_date')
        count_posts = post_list.count()
        paginator = Paginator(post_list, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        context = {
            'user': user,
            'author': author,
            'page': page,
            'count_posts': count_posts,
        }
        return render(request, 'profile.html', context)
    return redirect('index')


@login_required
def post_view(request, username, post_id):
    if request.method == 'GET':
        user = request.user
        author = User.objects.get(username=username)
        post = Post.objects.get(id=post_id)
        count_posts = Post.objects.filter(author_id=author.id).count()
        context = {
            'user': user,
            'author': author,
            'post': post,
            'count_posts': count_posts,
        }
        return render(request, 'post.html', context)
    return redirect('index')


@login_required
def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    user = request.user
    author = User.objects.get(username=username)
    if request.method == 'GET' and user.id == author.id:
        post = Post.objects.get(id=post_id)
        form = PostForm({
            'text': post.text,
            'pub_date': post.pub_date,
            'author': post.author,
            # 'group': post.group,
        })
        return render(request, 'new_post.html', {'form': form})
    return redirect('index')
