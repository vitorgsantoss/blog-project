from django.db import models
from util.rands import slugfy_new
from django.contrib.auth.models import User

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

        super().save(*args, **kwargs)