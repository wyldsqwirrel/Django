from django.db import models
from django.utils import timezone
from datetime import timedelta

class Email(models.Model):
    CATEGORIES = (
        ('urgent_important', 'Urgent & Important'),
        ('important_not_urgent', 'Important, Not Urgent'),
        ('urgent_not_important', 'Urgent, Not Important'),
        ('not_urgent_not_important', 'Not Urgent, Not Important'),
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.EmailField()
    recipient = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    synced = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, default='not_urgent_not_important')

    def __str__(self):
        return self.subject

    def auto_categorize(self):
        if "urgent" in self.subject.lower() or "asap" in self.body.lower():
            if "important" in self.subject.lower() or "priority" in self.body.lower():
                self.category = 'urgent_important'
            else:
                self.category = 'urgent_not_important'
        else:
            if "important" in self.subject.lower() or "priority" in self.body.lower():
                self.category = 'important_not_urgent'
            else:
                self.category = 'not_urgent_not_important'
        self.save()

from django.db import models
from django.utils import timezone

class Task(models.Model):
    STATUS_CHOICES = (
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
    )
    title = models.CharField(max_length=255)
    due_by = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    related_email = models.ForeignKey('Email', on_delete=models.SET_NULL, null=True, blank=True)
    depends_on = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    follow_up_after = models.IntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')

    def __str__(self):
        return self.title

    def check_follow_up(self):
        if not self.completed_at and self.related_email:
            delta = timezone.now() - self.related_email.created_at
            if delta.days >= self.follow_up_after:
                Task.objects.get_or_create(
                    title=f"Follow up on {self.related_email.subject}",
                    due_by=timezone.now() + timezone.timedelta(days=1),
                    related_email=self.related_email,
                    status='to_do'
                )
