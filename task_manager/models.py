from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="workers")

    def get_absolute_url(self):
        return reverse("task_manager:worker-detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"


PRIORITY_CHOICES = [
    ("URGENT", "Urgent"),
    ("HIGH", "High"),
    ("MEDIUM", "Medium"),
    ("LOW", "Low"),
]


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="MEDIUM",
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")
