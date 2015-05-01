# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import json
from django.template import RequestContext
from datetime import datetime
# from urllib.request import urlopen

def home(request):
  obj = {
    'page_title': 'Igor Stepanov',
  }
  return render(request, 'index.html', obj)

def gsoc(request):
  obj = {
    'fa': 'code',
    'page_title': 'Google Summer of Code 2015',
  }
  return render(request, 'gsoc15.html', obj)

def about(request):
  obj = {
    'fa': 'user',
    'page_title': 'About me',
  }
  return render(request, 'about.html', obj)

def scrobbler(request):
  obj = {
    'fa': 'lastfm-square',
    'page_title': 'Scrobbler',
  }
  return render(request, 'scrobbler.html', obj)

def schedule(request):
  curr_week = (datetime.now().isocalendar()[1] - 1) % 2 == 0
  count_week = datetime.now().isocalendar()[1] - datetime(2014, 9, 1).isocalendar()[1]
  obj = {
    'curr_week': curr_week,
    'fa': 'table',
    'page_title': 'Schedule',
  }
  return render(request, 'schedule.html', obj)

def base(request):
  return render(request, 'base.html')

def projects(request):
  obj = {
    'fa': 'code',
    'page_title': 'Projects',
  }
  return render(request, 'projects.html', obj)

def handler404(request):
  return render(request, '404.html')

def handler500(request):
  return render(request, '500.html')
