from django.contrib import admin
from django.utils import timezone

from .filter_utils import OverdueFilter
from .models import Task, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "project", "assigned_to", "status", "priority", "due_date"]
    list_filter = ["status", "priority", "project", OverdueFilter]
    search_fields = ["name", "description"]
    autocomplete_fields = ["assigned_to", "project", "tags"]
    ordering = ["due_date", "priority"]
    date_hierarchy = "due_date"
    readonly_fields = ["created_at", "updated_at"]
    actions = ["mark_completed"]
    
    @admin.action(description="Mark selected tasks as Completed")
    def mark_completed(modeladmin, request, queryset):
        queryset.update(status="completed")
