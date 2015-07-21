# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from taggit.models import Tag
import pytz
from django.views.decorators.cache import never_cache
import collections
from datetime import datetime, date

def index(request, page=1):
  posts_list = Post.objects.all().order_by('-pub_date')
  paginator = Paginator(posts_list, 10)

  # page = request.GET.get('page')
  try:
    posts_list = paginator.page(page)
  except PageNotAnInteger:
    posts_list = paginator.page(1)
  except EmptyPage:
    posts_list = paginator.page(paginator.num_pages)
  context = {
    'posts': posts_list,
    'page_title': 'Blog',
  }
  return render(request, 'blog/index.html', context)

def detail(request, post_id=1):
  post_id = int(post_id)
  # print post_id
  post = get_object_or_404(Post, pk=post_id)
  try:
    prev = Post.objects.get(pk=post_id-1)
  except Post.DoesNotExist:
    prev = False
  try:
    next = Post.objects.get(pk=post_id+1)
  except Post.DoesNotExist:
    next = False

  obj = {
    'post': post,
    'prev': prev,
    'next': next,
    'page_title': post.title,
  }
  return render(request, 'blog/detail.html', obj)

@never_cache
def archive(request):
  post = Post.objects.all().order_by('-pub_date')
  archive = list()
  for item in post:
    archive.append({
      'post': item, 
      'year': item.pub_date.date().year,
    })

  obj = {
    'archive': archive,
    'page_title': "Archive",
  }
  return render(request, 'blog/archive.html', obj)

def tags(request):
  tags = Tag.objects.all()
  obj = {
    'tags': tags,
    'page_title': "Tags",
  }
  return render(request, 'blog/tags.html', obj)

def tag(request, slug=""):
  posts = Post.objects.filter(tags__slug=slug).order_by('-pub_date')
  obj = {
    'posts': posts,
    'page_title': slug,
  }
  return render(request, 'blog/tag.html', obj)
