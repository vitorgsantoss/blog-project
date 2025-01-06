from django.db import models
from util.rands import slugfy_new

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