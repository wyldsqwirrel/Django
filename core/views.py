from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # ✅ Import added
from django.contrib.auth.views import LoginView
from django.template.exceptions import TemplateDoesNotExist
import logging
from tasks.models import Task
from recruitment.models import Candidate, Company
from django.conf import settings

logger = logging.getLogger(__name__)

# ----------------
#   HOME VIEW
# ----------------
def home(request):
    if request.user.is_authenticated:
        message = f"Welcome to Nutcrakka, {request.user.username}!"
    else:
        message = "Welcome to Nutcrakka! Please log in."

    return render(request, "core/home.html", {"message": message})  # ✅ Ensure home.html exists


# ----------------
#   SIGNUP VIEW
# ----------------
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login after signup
    else:
        form = UserCreationForm()

    return render(request, "core/signup.html", {"form": form})

# -----------------
#   LOGIN VIEW
# -----------------
def login(request):
    """
    Render the login page.
    """
    try:
        return render(request, "auth/login.html", {})
    except TemplateDoesNotExist as e:
        logger.warning(f"Template missing: {e}")
        return render(
            request, "crm/error.html", {"error_message": "Login template not found."}
        )


# ----------------
#   DASHBOARD VIEW (Fixed)
# ----------------
@login_required # ✅ Now correctly imported
def dashboard(request):
    """
    Render the global dashboard with data from multiple models.
    Handles missing templates gracefully.
    """
    try:
        tasks = Task.objects.filter(user=request.user, completed__at=False).order_by("due_by")

        candidate_limit = getattr(settings, "DASHBOARD_CANDIDATE_LIMIT", 5)
        company_limit = getattr(settings, "DASHBOARD_COMPANY_LIMIT", 5)

        candidates = Candidate.objects.all().order_by("-created_at")[:candidate_limit]
        companies = Company.objects.all().order_by("-created_at")[:company_limit]

        context = {
            "user": request.user,
            "tasks": tasks,
            "candidates": candidates,
            "companies": companies,
        }

        return render(request, "core/dashboard.html", context)  # ✅ Correct template path

    except TemplateDoesNotExist as e:
        logger.warning(f"Template missing: {e}")
        return render(
            request,
            "crm/error.html",
            {"error_message": "Dashboard template not found."},
        )

# ----------------
#   LOGOUT VIEW
# ----------------
def logout_view(request):
    logout(request)
    return redirect("login")  # Redirect users to login after logout

def apply_for_job(request, job_id):
    job = Job.objects.get(id=job_id)

    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()

            # Send confirmation email asynchronously via Celery
            send_email_task.delay(
                application.email, "Your job application has been received!"
            )

            messages.success(request, "Application submitted successfully!")
            return redirect("job_applied")
    else:
        form = JobApplicationForm()

    return render(request, "core/apply_for_job.html", {"form": form, "job": job})


from tasks.tasks import process_pending_applications  # Celery background task



# -----------------
#   HELPER FUNCTION
# -----------------
def get_user_emails(user):
    return [
        {
            "subject": "Welcome!",
            "sender": "admin@example.com",
            "received_at": "2025-01-01 10:00",
        },
        {
            "subject": "New Tasks Assigned",
            "sender": "tasks@example.com",
            "received_at": "2025-01-02 14:00",
        },
    ]


