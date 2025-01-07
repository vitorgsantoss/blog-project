from django.contrib import admin
from blog.models import Tag, Category, Page, Post
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'id','name','slug',
    list_display_links = 'name',
    search_fields= 'id','name','slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id','name','slug',
    list_display_links = 'name',
    search_fields= 'id','name','slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',),
    }

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = 'id', 'title', 'slug', 'is_published',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'slug',
    list_filter = 'is_published',
    list_editable = 'is_published',
    ordering = '-id',
    list_per_page = 10
    prepopulated_fields = {
        'slug': ('title',),
    }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'id','title', 'slug', 'created_by', 'is_published', 'cover_in_post_content',
    list_display_links = 'title',
    search_fields = 'id', 'title', 'slug', 'excerpt', 'content', ''
    list_editable = 'is_published', 'cover_in_post_content',
    list_per_page = 50
    orderin = '-id',
    list_filter = 'category', 'is_published', 'cover_in_post_content',
    readonly_fields = 'created_at', 'updated_at', 'created_by', 'updated_by',
    prepopulated_fields = {
        'slug': ('title',)
    }
    autocomplete_fields = 'category', 'tags',
