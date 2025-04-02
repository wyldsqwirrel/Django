# core/task_views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Email
from .forms import TaskForm, EmailForm
from .utils import get_pomodoro_context

@login_required
def task_list(request):
    tasks = request.user.tasks.all()
    context = {
        'tasks': tasks,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/task_list.html', context)

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('core:task_list')
    else:
        form = TaskForm()
    context = {
        'form': form,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/task_form.html', context)

@login_required
def email_list(request):
    emails = request.user.emails.all()
    context = {
        'emails': emails,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/email_list.html', context)

@login_required
def email_create(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.user = request.user
            email.save()
            messages.success(request, "Email created successfully!")
            return redirect('core:email_list')
    else:
        form = EmailForm()
    context = {
        'form': form,
        'pomodoro': get_pomodoro_context(),
    }
    return render(request, 'core/email_form.html', context)
