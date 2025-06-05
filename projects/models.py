from django.db import models
from django.conf import settings


class Project(models.Model):
    VISIBILITY_CHOISES = [
        ("private", "Private"),
        ("team", "Team Only"),
        ("public", "Public"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT, related_name="owned_projects")
    tech_stack = models.CharField(
        max_length=300, blank=True, help_text="e.g. Python, Django, React")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectMembership", related_name="projects")

    visibility = models.CharField(
        max_length=10, choices=VISIBILITY_CHOISES, default="private")
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ("owner", "Owner"),
        ("admin", "Admin"),
        ("member", "Member"),
        ("viewer", "Viewer"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="member")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["project", "user"]

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"
