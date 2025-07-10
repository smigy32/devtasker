from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

from .models import Task
from projects.models import Project


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["name", "description", "assigned_to", "status", "priority", "due_date", "tags"]
    template_name = "tasks/task_form.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs.get("project_id"))
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("projects:project_detail", args=[self.project.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    fields = "tasks/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    fields = ["name", "description", "assigned_to", "status", "priority", "due_date", "tags"]
    template_name = "tasks/task_form.html"
    context_object_name = "task"
    
    def test_func(self):
        task = self.get_object()
        user = self.request.user
        return task.project.members.filter(pk=user.pk).exists()
    
    def get_success_url(self):
        return reverse("tasks:task_detail", args=[self.object.pk])
    
from django.views.generic.edit import DeleteView

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    context_object_name = "task"

    def test_func(self):
        task = self.get_object()
        membership = task.project.projectmembership_set.filter(user=self.request.user).first()
        return membership and membership.role in ["admin", "owner"]

    def get_success_url(self):
        return reverse("projects:project_detail", args=[self.object.project.pk])

    
