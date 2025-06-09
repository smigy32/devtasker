from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import Project, ProjectMembership


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Project.objects.all()
        return user.projects.all()


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ["name", "description", "tech_stack", "visibility"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        ProjectMembership.objects.create(
            project=form.instance,
            user=self.request.user,
            role="owner"
        )
        return response
    

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ["name", "description", "tech_stack", "visibility", "is_archieved"]
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("projects:project_list")
    
    def test_func(self):
        project = self.get_object()
        membership = ProjectMembership.objects.get(project=project, user=self.request.user)
        return membership and membership.role in ["admin", "owner"]
    

class PrpjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("projects:project_list")
    
    def test_func(self):
        project = self.get_object()
        membership = ProjectMembership.objects.get(project=project, user=self.request.user)
        return membership and membership.role in ["admin", "owner"]
