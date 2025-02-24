from django.db import models
from django.contrib.auth.models import User
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
    synced = models.BooleanField(default=False)  # Two-way sync simulation
    category = models.CharField(max_length=50, choices=CATEGORIES, default='not_urgent_not_important')

    def __str__(self):
        return self.subject

    def auto_categorize(self):
        # Simple AI simulation: categorize based on keywords
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

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_by = models.DateTimeField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)
    related_email = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True, blank=True)
    depends_on = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Task dependency
    follow_up_after = models.IntegerField(default=3)  # Days for follow-up

    def __str__(self):
        return self.title

    def check_follow_up(self):
        if not self.completed_at and self.related_email:
            delta = timezone.now() - self.related_email.created_at
            if delta.days >= self.follow_up_after:
                # Simulate follow-up task creation
                Task.objects.get_or_create(
                    title=f"Follow up on {self.related_email.subject}",
                    due_by=timezone.now() + timedelta(days=1),
                    assigned_to=self.assigned_to,
                    related_email=self.related_email
                )
