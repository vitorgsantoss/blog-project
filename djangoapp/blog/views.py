from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from blog.models import Post,Page
from django.db.models import Q
from django.http import Http404, HttpRequest
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


class SearchListView(PostListView):
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        q = super().get_queryset().filter(
            Q(title__icontains = self.search_value) |
            Q(excerpt__icontains = self.search_value) |
            Q(created_by__first_name__icontains = self.search_value) |
            Q(created_by__last_name__icontains = self.search_value) |
            Q(category__name__icontains = self.search_value) |
            Q(tags__name__icontains = self.search_value))
        return q
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': f'{self.search_value} - '
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


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

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