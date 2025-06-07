from django.contrib import admin
from .models import Task, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "assigned_to", "status", "priority", "due_date"]
    list_filter = ["status", "priority", "project"]
    search_fields = ["name", "description"]
    autocomplete_fields = ["assigned_to", "project", "tags"]
    ordering = ["due_date", "priority"]
    date_hierarchy = "due_date"
