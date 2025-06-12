from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm
from .models import User


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request, "Your account has been created. You can now log in.")
        return super().form_valid(form)
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "bio", "job_title", "avatar"]
    template_name ="accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")
    
    def get_object(self):
        return self.request.user
