from django.db import models
from django.contrib.auth.models import User

class Email(models.Model):
    URGENCY_CHOICES = [
        (1, "Urgent & Important"),
        (2, "Important, Not Urgent"),
        (3, "Urgent, Not Important"),
        (4, "Neither Urgent Nor Important"),
    ]
    STATUS_CHOICES = [
        ("unsorted", "Unsorted"),
        ("todo", "To-Do"),
        ("in_progress", "In Progress"),
        ("waiting", "Waiting"),
        ("done", "Done"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    urgency = models.IntegerField(choices=URGENCY_CHOICES, default=4)
    is_task = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="unsorted")

    def __str__(self):
        return f"{self.subject} - {self.get_urgency_display()}"

class Task(models.Model):
    PRIORITY_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]
    
    STATUS_CHOICES = [
        ("backlog", "Backlog"),
        ("todo", "To-Do"),
        ("in_progress", "In Progress"),
        ("waiting", "Waiting"),
        ("done", "Done"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="backlog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
