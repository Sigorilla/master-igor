# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
import pytz
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views import generic

import collections
from datetime import datetime, date

from blog.models import Post
from blog.forms import *
from taggit.models import Tag


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url=reverse_lazy("blog:index"))


class NeverCacheMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(NeverCacheMixin, cls).as_view(**initkwargs)
        return never_cache(view)


class BlogList(NeverCacheMixin, generic.ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['page_title'] = 'Blog'
        return context


class PostView(NeverCacheMixin, generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['page_title'] = self.get_object().title
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_create_form'


class PostEditView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_create_form'


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

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

class TagList(NeverCacheMixin, generic.ListView):
    model = Tag
    template_name = "blog/tags.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['page_title'] = 'Tags'
        return context

def tag(request, slug=""):
    posts = Post.objects.filter(tags__slug=slug).order_by('-pub_date')
    obj = {
        'posts': posts,
        'page_title': slug,
    }
    return render(request, 'blog/tag.html', obj)
