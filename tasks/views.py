from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from .forms import TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def run_process_jobs(request):
    # Example function to process jobs (modify as needed)
    response_data = {"message": "Jobs processed successfully"}
    return JsonResponse(response_data)

@csrf_exempt
def run_task(request):
    """
    Dummy function to simulate running a task.
    """
    if request.method == "POST":
        # Example: Creating a test task
        task = Task.objects.create(name="New Task", status="pending")
        return JsonResponse({"message": f"Task {task.name} created successfully!"})
    
    return JsonResponse({"error": "Invalid request method"}, status=400)

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from tasks.models import Task
from tasks.forms import TaskForm

def task_update(request, pk):
    """
    View to update an existing task.
    """
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")  # ✅ Redirect to task list after update
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form, "task": task})

def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()

def create_completed_subtask():
    return "Subtask created successfully"

    return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
