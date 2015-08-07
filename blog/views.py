# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.http import Http404

import re

from blog.forms import *
from taggit.models import Tag


class SearchMixin(object):

    @staticmethod
    def normalize_query(query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        return [normspace(' ', (t[0] or t[1]).strip())
                for t in findterms(query_string)]

    def get_query(self, query_string, search_fields):
        # Query to search for every search term
        query = None
        terms = self.normalize_query(query_string)
        for term in terms:
            # Query to search for a given term in each field
            or_query = None
            for field_name in search_fields:
                q = Q(**{"%s__icontains" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query | or_query
        return query


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


class PostListView(NeverCacheMixin, generic.ListView):
    model = Post
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        # context['page_title'] = 'Blog'
        return context


class PostDetailView(NeverCacheMixin, generic.DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        get = super(PostDetailView, self).get(request, *args, **kwargs)
        if not (request.user.is_staff or self.object.active):
            raise PermissionDenied
        return get

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_staff or self.object.active:
            context['page_title'] = self.get_object().title
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Create post'
        context['fa'] = 'plus-circle'
        return context


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Edit post'
        context['fa'] = 'edit'
        return context


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data(**kwargs)
        context['page_title'] = 'Delete post'
        context['fa'] = 'trash'
        return context


class SearchPostListView(SearchMixin, NeverCacheMixin, generic.ListView):
    model = Post
    template_name = 'blog/search_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q'].strip()
            entry_query = self.get_query(
                query_string, ['title', 'intro', 'post'])
            return Post.objects.filter(entry_query).order_by('-pub_date')
        else:
            return Post.objects.all()

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            self.template_name = 'blog/search_post_ajax.html'
        return super(SearchPostListView, self).render_to_response(
            context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchPostListView, self).get_context_data(**kwargs)
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            context['query'] = self.request.GET['q'].strip()
            context['page_title'] = self.request.GET['q'].strip()
        else:
            context['query'] = ''
            context['page_title'] = 'Search'
        context['fa'] = 'search'
        return context


class TagListView(NeverCacheMixin, generic.ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['page_title'] = 'Tags'
        context['fa'] = 'tags'
        return context


class PostByTagListView(NeverCacheMixin, generic.ListView):
    model = Post
    template_name = 'blog/tag_detail.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PostByTagListView, self).get_context_data(**kwargs)
        try:
            tag = Tag.objects.get(slug=self.kwargs['slug'])
            context['page_title'] = tag.name
        except Tag.DoesNotExist:
            raise Http404
        context['fa'] = 'tag'
        return context


class SearchTagListView(SearchMixin, NeverCacheMixin, generic.ListView):
    model = Tag
    template_name = 'blog/search_tag_ajax.html'
    context_object_name = 'tags'

    def get_queryset(self):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q'].strip()
            entry_query = self.get_query(query_string, ['name'])
            return Tag.objects.filter(entry_query)
        else:
            return Tag.objects.all()

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            self.template_name = 'blog/search_tag_ajax.html'
        return super(SearchTagListView, self).render_to_response(
            context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchTagListView, self).get_context_data(**kwargs)
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            context['query'] = self.request.GET['q'].strip()
            context['page_title'] = self.request.GET['q'].strip()
        else:
            context['query'] = ''
            context['page_title'] = 'Search'
        context['fa'] = 'search'
        return context
