# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from fitness.models import Exercise, Training, Day
from django.views.generic import ListView
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import urllib2
import json

class FitnessView(ListView):
    model = Training
    template_name = "fitness/index.html"

    def get_context_data(self, **kwargs):
        context = super(FitnessView, self).get_context_data(**kwargs)
        context.update({u'page_title': 'Training'})
        context.update({u'fa': 'heartbeat'})

        context['day_list'] = Day.objects.all()
        countDays = len(context['day_list'])

        context['objects'] = {}
        context['no_exercise'] = []
        for training in context['object_list']:
            context['objects'].setdefault(training.exercise, []).append(training)
            if training.exercise.id not in context['no_exercise']:
                context['no_exercise'].append(training.exercise.id)

        context['exercise_list'] = Exercise.objects.exclude(pk__in=context['no_exercise'])
        for exercise in context['exercise_list']:
            context['objects'].setdefault(exercise, ['empty']*countDays)

        sorted(context['objects'])

        # check and add empty cells
        for exercise, trainings in context['objects'].items():
            for i in xrange(0, countDays):
                try:
                    if trainings[i] is not 'empty':
                        if (trainings[i].day != context['day_list'][i]):
                            context['objects'][exercise].insert(i, 'empty')
                except IndexError, e:
                    context['objects'][exercise].insert(i, 'empty')
                i += 1

        return context

@never_cache
@login_required
def save_results(request):
    data = {}
    if request.method == 'POST':
        trainingID = request.POST['trainingID']
        exerciseID = int(request.POST['exerciseID'])
        dayID = int(request.POST['dayID'])
        results = request.POST.get('results', False)
        if not trainingID:
            exercise, created = Exercise.objects.get_or_create(pk=exerciseID)
            day, created = Day.objects.get_or_create(pk=dayID)
            training = Training(
                exercise=exercise, 
                day=day, 
                results=results
            )
            training.save()
        else:
            training, created = Training.objects.update_or_create(
            pk=int(trainingID), defaults={'results': results})
            if created:
                data['created'] = True
        data['success'] = trainingID
    else:
        data['error'] = 'It is GET method'

    return JsonResponse(data)
