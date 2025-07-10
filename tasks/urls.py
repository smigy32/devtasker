from django.urls import path

from . import views


app_name = "tasks"

urlpatterns = [
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("projects/<int:project_id>/tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
]