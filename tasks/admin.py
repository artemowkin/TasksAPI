from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'owner')
    search_fields = ('title', 'subtitle')

