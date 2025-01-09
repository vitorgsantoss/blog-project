from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('created_by/<int:author_pk>/', 
        views.CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('page/', views.page, name='page'),
    path('post/<slug:slug>/', views.post, name='post'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('search/', views.search, name='search'),
]


