from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


app_name = "accounts"

urlpatterns = [
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="accounts/login.html", next_page="projects:project_list"), name="login"),
    path("logout/", LogoutView.as_view(next_page="accounts:login"), name="logout"),
]