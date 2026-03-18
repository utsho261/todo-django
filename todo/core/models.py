from django.db import models

# Create your models here.
class Priority(models.TextChoices):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Status(models.TextChoices):
    ACTIVE = 'Active'
    COMPLETED = 'Completed'

class Task(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=12, choices=Priority.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.title


