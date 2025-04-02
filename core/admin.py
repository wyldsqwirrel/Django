# core/admin.py
from django.contrib import admin
from .models import Task, Email, Board, BoardItem, Note

# Register Task and Email (moved from tasks/admin.py)
admin.site.register(Task)
admin.site.register(Email)

# Register Productivity models
admin.site.register(Board)
admin.site.register(BoardItem)
admin.site.register(Note)
