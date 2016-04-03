# -*- coding: utf-8 -*-
from django.shortcuts import render
from datetime import datetime


def home(request):
    obj = {
        'page_title': 'Igor Stepanov',
    }
    return render(request, 'vcard_sigorilla.html', obj)


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


def travel(request):
    obj = {
        'fa': 'globe',
        'page_title': 'Travel',
    }
    return render(request, 'travel.html', obj)


def scrobbler(request):
    obj = {
        'fa': 'lastfm-square',
        'page_title': 'Scrobbler',
    }
    return render(request, 'scrobbler.html', obj)


def schedule(request):
    curr_week = (datetime.now().isocalendar()[1] - 1) % 2 == 0
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


def handler403(request):
    obj = {
        'fa': 'exclamation-circle',
        'page_title': '403: Forbidden',
    }
    return render(request, '403.html', obj)


def handler404(request):
    obj = {
        'fa': 'exclamation-circle',
        'page_title': '404: Not Found',
    }
    return render(request, '404.html', obj)


def handler500(request):
    obj = {
        'fa': 'exclamation-triangle',
        'page_title': '500: Internal Server Error',
    }
    return render(request, '500.html', obj)
