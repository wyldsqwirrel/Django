from tasks.models import Task
from datetime import datetime, timedelta

def task_summary(request):
    if request.user.is_authenticated:
        today = datetime.now().date()
        upcoming_tasks = Task.objects.filter(
            assigned_to=request.user,
            completed_at__isnull=True,
            due_by__gte=today,
            due_by__lte=today + timedelta(days=7)
        ).order_by('due_by')[:5]
        return {'task_summary': upcoming_tasks}
    return {}