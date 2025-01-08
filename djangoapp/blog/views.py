from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from blog.models import Post
from django.db.models import Q

# Create your views here.


def index(request):
    posts = Post.objects.filter(is_published = True)
    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
        }
    )

def page(request):

    return render(
        request,
        'blog/pages/page.html',
        {
            # 'page_obj': page_obj,
        }
    )

def post(request, slug):
    post = Post.objects.filter(
        is_published = True
        ).filter(slug=slug).first()

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.filter(
        is_published = True).filter(created_by__pk = author_pk)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )


def category(request, slug):
    posts = Post.objects.filter(
        is_published = True
        ).filter(category__slug = slug)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )


def tag(request, slug):
    posts = Post.objects.filter(
        is_published = True
        ).filter(tags__slug = slug)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()

    if search_value == '':
        return redirect('blog:index')
    
    posts = Post.objects.filter(
        is_published = True
        ).filter(
            Q(title__icontains = search_value) |
            Q(excerpt__icontains = search_value) |
            Q(created_by__first_name__icontains = search_value) |
            Q(created_by__last_name__icontains = search_value) |
            Q(category__name__icontains = search_value) |
            Q(tags__name__icontains = search_value)

        )
    
    print('posts:', posts)
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )