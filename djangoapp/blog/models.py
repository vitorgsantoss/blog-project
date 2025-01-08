from django.db import models
from util.rands import slugfy_new
from util.image import resize_image
from django.contrib.auth.models import User
from django_summernote.models import AbstractAttachment
from django.urls import reverse


# Create your models here.

    

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name, len = 8)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
        )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.name, len = 8)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
        )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisa estar habilitado para que a página seja exibida.'
        )
    )
    content = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.title, len = 8)
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class PostAttachment(AbstractAttachment):
    def save(self, *args, **kwargs):
        current_file_name = str(self.file.name)
        super_save = super().save(*args, **kwargs)
        file_changed = False

        if self.file:
            file_changed = current_file_name != self.file.name
        
        if file_changed:
            resize_image(self.file, 900)
        super().save(*args, **kwargs)



class Post(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )
    excerpt = models.CharField(max_length=255)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            'Este campo precisa ser estar marcado'
            'para que o campo seja exibido publicamente'
    ),)
    content = models.TextField()
    cover = models.ImageField(blank=True, upload_to='posts/')
    cover_in_post_content = models.BooleanField(
        default=False,
        help_text='Se marcado, exibe a capa no conteúdo do post.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null = True, 
        blank = True,
        related_name='post_created_by',
        )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null = True, 
        blank = True,
        related_name='post_updated_by',
        )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugfy_new(self.title, 8)
        
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        
        if cover_changed:
            resize_image(self.cover, 900)
        
        return super_save
    

    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))
    

    
