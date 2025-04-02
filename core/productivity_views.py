# core/productivity_views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Board, BoardItem, Note
from .forms import BoardItemForm, NoteForm
from .utils import get_pomodoro_context
from rest_framework import viewsets
from .serializers import NoteSerializer

@login_required
def productivity_dashboard(request):
    tasks = request.user.tasks.filter(completed=False).order_by("due_date")  # Updated
    boards = request.user.boards.all()  # Updated
    notes = request.user.notes.all()  # Updated
    context = {
        'tasks': tasks,
        'boards': boards,
        'notes': notes,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/productivity_dashboard.html', context)

@login_required
def board_detail(request, pk):
    board = request.user.boards.get(pk=pk)  # Updated
    if request.method == "POST":
        form = BoardItemForm(request.POST)
        if form.is_valid():
            board_item = form.save(commit=False)
            board_item.board = board
            board_item.save()
            messages.success(request, "Item added to board!")
            return redirect('core:board_detail', pk=pk)
    else:
        form = BoardItemForm()
    context = {
        'board': board,
        'form': form,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/board_detail.html', context)

@login_required
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note created successfully!")
            return redirect('core:productivity_dashboard')
    else:
        form = NoteForm()
    context = {
        'form': form,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/note_form.html', context)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_queryset(self):
        return self.request.user.notes.all()  # Updated
