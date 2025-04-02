# core/forms.py
from django import forms
from .models import Task, Email, BoardItem, Note

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'completed']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['subject', 'sender', 'content']  # Remove 'received_at'
        # No widget needed for 'received_at' since it's removed

class BoardItemForm(forms.ModelForm):
    class Meta:
        model = BoardItem
        fields = ['content', 'position_x', 'position_y']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'handwritten_image']
        widgets = {
            'handwritten_image': forms.ClearableFileInput(),
        }
