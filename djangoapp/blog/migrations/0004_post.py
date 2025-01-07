# Generated by Django 5.1.4 on 2025-01-07 01:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_page'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True)),
                ('excerpt', models.CharField(max_length=255)),
                ('is_published', models.BooleanField(default=False, help_text='Este campo precisa ser estar marcadopara que o campo seja exibido publicamente')),
                ('content', models.TextField()),
                ('cover', models.ImageField(blank=True, upload_to='posts/')),
                ('cover_in_post_content', models.BooleanField(default=False, help_text='Se marcado, exibe a capa no conteúdo do post.')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_created_by', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, default='', to='blog.tag')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]