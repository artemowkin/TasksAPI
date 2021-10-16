from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskModel(admin.ModelAdmin):
    list_fields = ('title', 'subtitle')
    search_fields = ('title', 'subtitle')

