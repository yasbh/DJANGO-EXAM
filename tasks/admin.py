
# Register your models here.
from django.contrib import admin
from .models import Task, Result

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'output', 'created_at')
    search_fields = ('output', 'task__title')
    autocomplete_fields = ('task',)
