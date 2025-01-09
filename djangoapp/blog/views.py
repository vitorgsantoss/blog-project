from typing import Any
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from blog.models import Post,Page
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView

# Create your views here.

PER_PAGE = 9

class PostListView(ListView):
    model = Post
    template_name =  'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    ordering = 'pk'
    queryset = Post.objects.filter(is_published = True)

# def index(request):
#     posts = Post.objects.filter(is_published = True)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'posts': page_obj,
#             'page_title': 'Home - ',
#         }
#     )

def page(request):
    page_obj = Page.objects.filter(
        is_published = True
    ).first()

    title = page_obj.title #type: ignore
    page_title = f'{title[:50]} - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def post(request, slug):
    post_obj = Post.objects.filter(
        is_published = True
        ).filter(slug=slug).first()
    
    post_title = post_obj.title #type: ignore
    page_title = f'{post_title[:50]} - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post_obj,
            'page_title': page_title,
        }
    )


def created_by(request, author_pk):
    posts = Post.objects.filter(
        is_published = True).filter(created_by__pk = author_pk)
    
    author_first_name = posts.first().created_by.first_name or '' #type: ignore
    author_last_name = posts.first().created_by.last_name or ''#type: ignore
    author_full_name = f'{author_first_name} {author_last_name}'
    
    if author_full_name.strip() == '':
        raise Http404()
    
    page_title = f'Posts de {author_full_name} - '

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def category(request, slug):
    posts = Post.objects.filter(
        is_published = True
        ).filter(category__slug = slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    post_category = posts.first().category.name #type: ignore
    page_title = f'Categoria - {post_category} - '
    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def tag(request, slug):
    posts = Post.objects.filter(
        is_published = True
        ).filter(tags__slug = slug)
    
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    post_tag = posts.first().tags.first().name #type: ignore
    page_title = f'Tag - {post_tag} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    page_title = f'{search_value} - '

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
    
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    
    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )