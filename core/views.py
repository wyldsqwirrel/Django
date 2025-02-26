from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.exceptions import TemplateDoesNotExist
import logging
from tasks.models import Task, Email
from marketing.models import Lead, Activity
from recruitment.models import Job, Candidate, Placement
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

logger = logging.getLogger(__name__)

@login_required
def home(request):
    tasks = Task.objects.filter(completed_at__isnull=True).order_by("due_by")[:5]
    context = {"user": request.user, "tasks": tasks}
    return render(request, "home.html", context)

@login_required
def dashboard(request):
    try:
        tasks = Task.objects.filter(completed_at__isnull=True).order_by("due_by")[:5]
        all_tasks = Task.objects.all().order_by("due_by")
        emails = Email.objects.all().order_by("-created_at")[:5]
        email_categories = {
            'urgent_important': Email.objects.filter(category='urgent_important'),
            'important_not_urgent': Email.objects.filter(category='important_not_urgent'),
            'urgent_not_important': Email.objects.filter(category='urgent_not_important'),
            'not_urgent_not_important': Email.objects.filter(category='not_urgent_not_important'),
        }
        leads = Lead.objects.all().order_by("-created_at")[:5]
        activities = Activity.objects.all().order_by("-date")[:5]
        all_activities = Activity.objects.all().order_by("date")
        jobs = Job.objects.all().order_by("-created_at")[:5]
        candidates = Candidate.objects.all().order_by("-created_at")[:5]
        placements = Placement.objects.all().order_by("-created_at")[:5]
        context = {
            "user": request.user,
            "tasks": tasks,
            "all_tasks": all_tasks,
            "emails": emails,
            "email_categories": email_categories,
            "leads": leads,
            "activities": activities,
            "all_activities": all_activities,
            "jobs": jobs,
            "candidates": candidates,
            "placements": placements,
        }
        return render(request, "dashboard.html", context)  # Changed to "dashboard.html"
    except TemplateDoesNotExist as e:
        logger.warning(f"Template missing: {e}")
        return render(request, "crm/error.html", {"error_message": "Dashboard template not found."})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
