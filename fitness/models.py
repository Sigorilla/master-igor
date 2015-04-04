from django.db import models
from datetime import datetime
import json

class Training(models.Model):

    class Meta:
        verbose_name = "Training"
        verbose_name_plural = "Trainings"
        ordering = ['exercise', 'day']
        unique_together = ('exercise', 'day')

    def __unicode__(self):
        return self.exercise.title

    exercise = models.ForeignKey('Exercise', default=True)
    results = models.TextField()
    day = models.ForeignKey('Day', default=True)

    def getResults(self):
        return json.loads(self.results);

class Exercise(models.Model):

    class Meta:
        verbose_name = "Exercise"
        verbose_name_plural = "Exercises"
        ordering = ['title']

    def __unicode__(self):
        return self.title

    title = models.CharField(default='Exercise', max_length=100, unique=True)
    description = models.TextField(blank=True)

class Day(models.Model):

    class Meta:
        verbose_name = "Day"
        verbose_name_plural = "Days"
        ordering = ['datetime']

    def __unicode__(self):
        return self.datetime.strftime('%d %B %Y %H:%M:%S')

    datetime = models.DateTimeField(default=datetime.now())
