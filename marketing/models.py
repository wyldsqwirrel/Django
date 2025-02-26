from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task

class Lead(models.Model):
    STATUS_CHOICES = (
        ('identified', 'Identified'),
        ('contacted', 'Contacted'),
        ('engaged', 'Engaged'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('deal_in_progress', 'Deal in Progress'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True)  # e.g., LinkedIn, Referral
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='identified')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('identified', 'Lead Identified'),
        ('linkedin_request', 'LinkedIn Connection Request'),
        ('linkedin_connected', 'LinkedIn Connected'),
        ('email_sent', 'Email Sent'),
        ('call_made', 'Call Made'),
        ('meeting_scheduled', 'Meeting Scheduled'),
        ('meeting_held', 'Meeting Held'),
        ('deal_proposed', 'Deal Proposed'),
        ('deal_closed', 'Deal Closed'),
        ('lost', 'Lost'),
    )
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.lead.name} - {self.get_activity_type_display()} ({self.date})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update lead status based on latest activity
        if self.activity_type in ['identified', 'linkedin_request', 'linkedin_connected', 'email_sent', 'call_made']:
            self.lead.status = 'contacted'
        elif self.activity_type == 'meeting_scheduled':
            self.lead.status = 'meeting_scheduled'
        elif self.activity_type == 'meeting_held':
            self.lead.status = 'engaged'
        elif self.activity_type == 'deal_proposed':
            self.lead.status = 'deal_in_progress'
        elif self.activity_type == 'deal_closed':
            self.lead.status = 'converted'
        elif self.activity_type == 'lost':
            self.lead.status = 'lost'
        self.lead.save()
