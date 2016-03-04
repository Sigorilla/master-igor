from django.contrib import admin
from fitness.models import Exercise, Training, Day


class ExerciseAdmin(admin.ModelAdmin):
    """
        Admin View for Exercise
    """
    list_display = ('title', 'description')
    search_fields = ['title']


class TrainingAdmin(admin.ModelAdmin):
    """
        Admin View for Training
    """
    list_display = ('exercise', 'results', 'day')
    list_filter = ('day',)
    search_fields = ['day']


class DayAdmin(admin.ModelAdmin):
    """
        Admin View for Day
    """
    list_display = ('datetime',)
    list_filter = ('datetime',)

admin.site.register(Day, DayAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Exercise, ExerciseAdmin)
