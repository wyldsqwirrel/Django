from django import forms
from .models import Task  # ✅ Ensure you import the correct model


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # ✅ Ensure this matches `models.py`
        fields = ["name", "description", "status", "due_date"]
