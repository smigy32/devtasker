from django.contrib import admin
from django.utils import timezone


class OverdueFilter(admin.SimpleListFilter):
    title = "Overdue"
    parameter_name = "overdue"

    def lookups(self, request, model_admin):
        return [
            ("yes", "Overdue"),
            ("no", "On time / No due date")
        ]

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == "yes":
            return queryset.filter(due_date__lt=today).exclude(status="completed")
        elif self.value() == "no":
            return queryset.exclude(due_date__lt=today) | queryset.filter(status="completed")
