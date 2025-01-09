from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from blog.models import Post,Page
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

# Create your views here.

PER_PAGE = 9

class PostListView(ListView):
    # model = Post
    template_name =  'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    ordering = 'pk'
    queryset = Post.objects.filter(is_published = True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Home - '
        })
        return context


class CreatedByListView(PostListView):    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author_pk = self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404
    
        if user.first_name:
            user_full_name = f'{user.first_name } {user.last_name} - '

        context.update({
            'page_title': user_full_name,
        })

        return context
    

    def get_queryset(self) -> QuerySet[Any]:
        q =  super().get_queryset()
        q = q.filter(created_by__pk = self.kwargs.get('author_pk'))
        return q
    

class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        q = super().get_queryset()
        q = q.filter(category__slug = self.kwargs.get('slug'))
        return q
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.object_list[0].category.name#type:ignore
        page_title = f'Categoria - {category_name} - '
        
        context.update({
            'page_title': page_title
        })
        return context


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        q = super().get_queryset()
        q = q.filter(tags__slug = self.kwargs.get('slug'))
        return q
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        slug = self.kwargs.get('slug')
        query_set_tag = self.object_list[0].tags.filter(slug = slug)#type:ignore
        tag_name = query_set_tag.first().name
        page_title = f'Tag - {tag_name} - '
        
        context.update({
            'page_title': page_title
        })
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_queryset(self) -> QuerySet[Any]:
        print(super().get_queryset())
        return super().get_queryset().filter(is_published = True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f'{page.title} - '#type:ignore

        context.update({
            'page_title': page_title
        })
        return context



# def page(request):
#     page_obj = Page.objects.filter(
#         is_published = True
#     ).first()

#     title = page_obj.title #type: ignore
#     page_title = f'{title[:50]} - '

#     return render(
#         request,
#         'blog/pages/page.html',
#         {
#             'page_obj': page_obj,
#             'page_title': page_title,
#         }
#     )


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
            'posts': page_obj,
            'page_title': page_title,
        }
    )