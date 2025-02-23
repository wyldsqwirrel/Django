from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings
import logging
from tasks.models import Task  # ✅ Correct import
from .models import Candidate, Company, Contact, Job, Placement, Interview
from .forms import (
    CandidateForm,
    CompanyForm,
    ContactForm,
    JobForm,
    PlacementForm,
    InterviewForm,
    JobApplicationForm,
)

logger = logging.getLogger(__name__)



def process_jobs_view(request):
    """
    This function triggers a Celery task to process pending job applications.
    """
    process_pending_applications.delay()  # Run task asynchronously
    messages.success(request, "Job applications are being processed!")
    return render(request, "recruitment/jobs_processed.html")


def job_applied(request):
    return render(request, "recruitment/job_applied.html")


# -----------------
#    LIST VIEWS
# -----------------
def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, "recruitment/candidate_list.html", {"candidates": candidates})


def company_list(request):
    companies = Company.objects.all()
    return render(request, "recruitment/company_list.html", {"companies": companies})


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "recruitment/contact_list.html", {"contacts": contacts})


def job_list(request):
    jobs = Job.objects.all()
    return render(request, "recruitment/job_list.html", {"jobs": jobs})


def interview_list(request):
    interviews = Interview.objects.all().order_by("-scheduled_date")
    return render(
        request, "recruitment/interview_list.html", {"interviews": interviews}
    )


def placement_list(request):
    placements = Placement.objects.all()
    return render(
        request, "recruitment/placement_list.html", {"placements": placements}
    )


# -----------------
#   CREATE VIEWS
# -----------------
def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("candidate_list")
    else:
        form = CandidateForm()
    return render(request, "recruitment/candidate_form.html", {"form": form})


def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("company_list")
    else:
        form = CompanyForm()
    return render(request, "recruitment/company_form.html", {"form": form})


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("contact_list")
    else:
        form = ContactForm()
    return render(request, "recruitment/contact_form.html", {"form": form})


def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobForm()
    return render(request, "recruitment/job_form.html", {"form": form})


def placement_create(request):
    if request.method == "POST":
        form = PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("placement_list")
    else:
        form = PlacementForm()
    return render(request, "recruitment/placement_form.html", {"form": form})


def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("interview_list")
    else:
        form = InterviewForm()
    return render(request, "recruitment/interview_form.html", {"form": form})


