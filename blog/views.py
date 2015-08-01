# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views import generic

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


class BlogList(NeverCacheMixin, generic.ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.objects.filter(active__exact=True)

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

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['page_title'] = 'Create post'
        context['fa'] = 'plus-circle'
        return context


class PostEditView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name_suffix = '_create_form'

    def get_context_data(self, **kwargs):
        context = super(PostEditView, self).get_context_data(**kwargs)
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
        'page_title': "",
    }
    return render(request, 'blog/archive.html', obj)


class SearchList(SearchMixin, NeverCacheMixin, LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q'].strip()
            entry_query = self.get_query(query_string, ['title', 'intro', 'post'])
            return Post.objects.filter(entry_query).order_by('-pub_date')
        else:
            self.paginate_by = None

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            self.template_name = 'blog/search_ajax.html'
        return super(SearchList, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
          context['query'] = self.request.GET['q'].strip()
          context['page_title'] = self.request.GET['q'].strip()
        else:
          context['query'] = ''
          context['page_title'] = 'Search'
        context['fa'] = 'search'
        return context


class TagList(NeverCacheMixin, generic.ListView):
    model = Tag
    template_name = "blog/tags.html"
    context_object_name = "tags"

    def get_context_data(self, **kwargs):
        context = super(TagList, self).get_context_data(**kwargs)
        context['page_title'] = 'Tags'
        context['fa'] = 'tags'
        return context


class SearchTagList(SearchMixin, generic.ListView):
    model = Tag
    template_name = 'blog/tags.html'
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
        return super(SearchTagList, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchTagList, self).get_context_data(**kwargs)
        if ('q' in self.request.GET) and self.request.GET['q'].strip():
          context['query'] = self.request.GET['q'].strip()
          context['page_title'] = self.request.GET['q'].strip()
        else:
          context['query'] = ''
          context['page_title'] = 'Search'
        context['fa'] = 'search'
        return context


def tag(request, slug=""):
    posts = Post.objects.filter(tags__slug=slug).order_by('-pub_date')
    obj = {
        'posts': posts,
        'page_title': slug,
        'fa':'tag',
    }
    return render(request, 'blog/tag.html', obj)
