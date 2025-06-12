from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request, "Your account has been created. You can now log in.")
        return super().form_valid(form)
