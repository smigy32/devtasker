from django.contrib import admin

from .models import Project, ProjectMembership


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "visibility", "created_at"]
    list_filter = ["visibility", "is_archived"]


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "project", "role", "joined_at"]
    list_filter = ["role"]
