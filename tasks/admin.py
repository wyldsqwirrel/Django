from django.contrib import admin
from .models import Task, Email

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'due_by', 'status', 'completed_at']
    list_filter = ['status', 'due_by', 'completed_at']
    search_fields = ['title']

class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['subject', 'sender', 'recipient']

admin.site.register(Task, TaskAdmin)
admin.site.register(Email, EmailAdmin)
