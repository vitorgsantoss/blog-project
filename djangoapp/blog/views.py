from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post

# Create your views here.
posts = list(range(1000))

def index(request):
    posts = Post.objects.get_published() #type: ignore

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
    post = Post.objects.get_published().filter(slug=slug).first() #type: ignore

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.get_published().filter(created_by__pk = author_pk) #type: ignore

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )


def category(request, slug):
    posts = Post.objects.get_published().filter(category__slug = slug) #type: ignore
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )


def tag(request, slug):
    posts = Post.objects.get_published().filter(tags__slug = slug) #type: ignore
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts
        }
    )