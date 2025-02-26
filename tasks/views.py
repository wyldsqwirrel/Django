from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Task, Email
from django.utils import timezone

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})
    category = request.GET.get('category', '')
    tasks = Task.objects.filter(assigned_to=request.user)
    if category:
        tasks = tasks.filter(related_email__category=category)
    emails = Email.objects.all()
    kanban_tasks = {
        'to_do': tasks.filter(status='to_do'),
        'in_progress': tasks.filter(status='in_progress'),
        'on_hold': tasks.filter(status='on_hold'),
        'completed': tasks.filter(status='completed'),
    }
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'emails': emails,
        'kanban_tasks': kanban_tasks,
        'category': category
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.check_follow_up()
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_by = request.POST['due_by']
        assigned_to = User.objects.get(id=request.POST['assigned_to'])
        related_email_id = request.POST.get('related_email')
        depends_on_id = request.POST.get('depends_on')
        follow_up_after = request.POST.get('follow_up_after', 3)
        status = request.POST.get('status', 'to_do')
        task = Task(
            title=title, due_by=due_by, assigned_to=assigned_to,
            related_email=Email.objects.get(id=related_email_id) if related_email_id else None,
            depends_on=Task.objects.get(id=depends_on_id) if depends_on_id else None,
            follow_up_after=follow_up_after, status=status
        )
        task.save()
        return redirect('tasks:task_list')
    users = User.objects.all()
    emails = Email.objects.all()
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/task_create.html', {'users': users, 'emails': emails, 'tasks': tasks})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_by = request.POST['due_by']
        task.assigned_to = User.objects.get(id=request.POST['assigned_to'])
        related_email_id = request.POST.get('related_email')
        depends_on_id = request.POST.get('depends_on')
        task.related_email = Email.objects.get(id=related_email_id) if related_email_id else None
        task.depends_on = Task.objects.get(id=depends_on_id) if depends_on_id else None
        task.follow_up_after = request.POST.get('follow_up_after', 3)
        task.status = request.POST.get('status', task.status)
        if 'completed' in request.POST:
            task.completed_at = timezone.now()
            if task.related_email:
                task.related_email.synced = True
                task.related_email.save()
            task.status = 'completed'
        else:
            task.completed_at = None
        task.save()
        return redirect('tasks:task_detail', task_id=task.id)
    users = User.objects.all()
    emails = Email.objects.all()
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/task_update.html', {'task': task, 'users': users, 'emails': emails, 'tasks': tasks})

@login_required
def email_list(request):
    emails = Email.objects.all()
    for email in emails:
        email.auto_categorize()
    return render(request, 'tasks/email_list.html', {'emails': emails})

@login_required
def email_create(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        body = request.POST['body']
        sender = request.POST['sender']
        recipient = request.POST['recipient']
        email = Email(subject=subject, body=body, sender=sender, recipient=recipient)
        email.save()
        email.auto_categorize()
        return redirect('tasks:email_list')
    return render(request, 'tasks/email_create.html')

@login_required
def update_category(request, task_id, category):
    task = get_object_or_404(Task, id=task_id)
    if task.related_email:
        task.related_email.category = category
        task.related_email.save()
    return HttpResponse(status=200)

@login_required
def update_email_category(request, email_id, category):
    email = get_object_or_404(Email, id=email_id)
    email.category = category
    email.save()
    # Create or update a related task
    task, created = Task.objects.get_or_create(
        related_email=email,
        assigned_to=request.user,
        defaults={
            'title': f"Action: {email.subject}",
            'due_by': timezone.now() + timedelta(days=1),
            'status': 'to_do'
        }
    )
    return HttpResponse(status=200)

@login_required
def update_task_status(request, task_id, status):
    task = get_object_or_404(Task, id=task_id)
    task.status = status
    if status == 'completed':
        task.completed_at = timezone.now()
    else:
        task.completed_at = None
    task.save()
    return HttpResponse(status=200)
