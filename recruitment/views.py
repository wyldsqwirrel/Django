# recruitment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings
from django.contrib import messages
import logging
from core.tasks import send_email_task, process_pending_applications  # Update import
from core.models import Task, Email
from .models import Candidate, Company, Contact, Job, Placement, Interview, Event
from .forms import CandidateForm, CompanyForm, ContactForm, JobForm, PlacementForm, InterviewForm, JobApplicationForm
import os
import csv
import uuid
import PyPDF2
import docx
from django.utils import timezone
from core.utils import get_pomodoro_context

logger = logging.getLogger(__name__)

# Rest of the file remains the same

def get_pomodoro_context():
    """
    Helper function to provide Pomodoro timer context.
    Replace with actual Pomodoro logic if needed (e.g., fetching from a model).
    """
    return {'work_duration': 25, 'break_duration': 5}

# Helper function to parse CV and store in attachments.csv
def parse_and_store_cv(cv_file):
    """
    Parses the uploaded CV file, extracts relevant fields, and stores it in attachments.csv.
    Returns a tuple of (cv_id, extracted_data).
    """
    # Generate a unique CV ID
    cv_id = str(uuid.uuid4())

    # Read the CV file content
    content = ""
    if cv_file.name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(cv_file)
        for page in pdf_reader.pages:
            content += page.extract_text()
    elif cv_file.name.endswith('.docx'):
        doc = docx.Document(cv_file)
        content = "\n".join([para.text for para in doc.paragraphs])
    else:  # Assume plain text
        content = cv_file.read().decode('utf-8', errors='ignore')

    # Simple parsing logic (you can enhance this based on your CV format)
    extracted_data = {
        'full_name': '',
        'email': '',
        'phone': '',
        'skills': '',
    }

    # Basic parsing: look for patterns in the content
    content_lower = content.lower()
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        # Extract full name (assuming it's one of the first lines)
        if not extracted_data['full_name'] and len(line.split()) >= 2 and '@' not in line:
            extracted_data['full_name'] = line
        # Extract email
        if '@' in line and not extracted_data['email']:
            extracted_data['email'] = line.split()[-1] if line.split() else ''
        # Extract phone (basic pattern matching)
        if any(char.isdigit() for char in line) and ('phone' in line.lower() or len([c for c in line if c.isdigit()]) >= 8):
            extracted_data['phone'] = line.split()[-1] if line.split() else ''
        # Extract skills (look for a "skills" section)
        if 'skills' in line.lower() and not extracted_data['skills']:
            extracted_data['skills'] = line.replace('skills', '', 1).strip()

    # Store the CV in attachments.csv
    csv_path = os.path.join(settings.BASE_DIR, "recruitment/csv/attachments.csv")
    file_exists = os.path.isfile(csv_path)
    with open(csv_path, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'filename', 'content', 'uploaded_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'id': cv_id,
            'filename': cv_file.name,
            'content': content,
            'uploaded_at': timezone.now().strftime('%Y-%m-d %H:%M:%S'),
        })

    return cv_id, extracted_data

# Helper function to fetch CV content
def get_cv_content(cv_id):
    """
    Fetches CV content from attachments.csv based on the CV ID.
    Returns a dictionary with CV details or None if not found.
    """
    if not cv_id:
        return None
    csv_path = os.path.join(settings.BASE_DIR, "recruitment/csv/attachments.csv")
    try:
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["id"] == cv_id:
                    return {
                        "id": row["id"],
                        "filename": row.get("filename", "Unknown"),
                        "content": row.get("content", "No content available"),
                        "uploaded_at": row.get("uploaded_at", "Unknown"),
                    }
    except (FileNotFoundError, KeyError):
        return None
    return None

def home(request):
    """
    Home view for the recruitment app.
    """
    try:
        context = {
            "user_emails": get_user_emails(request.user),
            "pomodoro": get_pomodoro_context(),
        }
        return render(request, "recruitment/home_dashboard.html", context)
    except TemplateDoesNotExist as e:
        logger.warning(f"Template missing: {e}")
        return render(request, "core/error.html", {"error_message": "Home template not found."})

@login_required
def dashboard(request):
    """
    Dashboard view displaying tasks, emails, calendar events, candidates, and companies.
    """
    try:
        tasks = Task.objects.filter(user=request.user, completed=False).order_by("due_date")
        user_emails = Email.objects.filter(user=request.user).order_by("-received_at")[:5]
        calendar_events = Event.objects.filter(user=request.user)
        candidate_limit = getattr(settings, "DASHBOARD_CANDIDATE_LIMIT", 5)
        company_limit = getattr(settings, "DASHBOARD_COMPANY_LIMIT", 5)
        candidates = Candidate.objects.all().order_by("-created_on")[:candidate_limit]
        companies = Company.objects.all().order_by("-created_on")[:company_limit]
        context = {
            "user": request.user,
            "tasks": tasks,
            "user_emails": user_emails,
            "calendar_events": calendar_events,
            "candidates": candidates,
            "companies": companies,
            "pomodoro": get_pomodoro_context(),
        }
        return render(request, "recruitment/dashboard.html", context)
    except TemplateDoesNotExist as e:
        logger.warning(f"Template missing: {e}")
        return render(request, "core/error.html", {"error_message": "Dashboard template not found."})

def apply_for_job(request, job_id):
    """
    View for applying to a specific job.
    """
    job = Job.objects.get(id=job_id)
    if request.method == "POST":
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            send_email_task.delay(application.email, "Your job application has been received!")
            messages.success(request, "Application submitted successfully!")
            return redirect("recruitment:job_applied")
    else:
        form = JobApplicationForm()
    context = {
        "form": form,
        "job": job,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/apply_for_job.html", context)

def process_jobs_view(request):
    """
    View to trigger processing of pending job applications.
    """
    process_pending_applications.delay()
    messages.success(request, "Job applications are being processed!")
    context = {
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/jobs_processed.html", context)

def job_applied(request):
    """
    Confirmation view after a job application is submitted.
    """
    context = {
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/job_applied.html", context)

# List Views
def candidate_list(request):
    """
    View to list all candidates.
    """
    candidates = Candidate.objects.all()
    context = {
        "candidates": candidates,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/candidate_list.html", context)

def company_list(request):
    """
    View to list all companies.
    """
    companies = Company.objects.all()
    context = {
        "companies": companies,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/company_list.html", context)

def contact_list(request):
    """
    View to list all contacts.
    """
    contacts = Contact.objects.all()
    context = {
        "contacts": contacts,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/contact_list.html", context)

def job_list(request):
    """
    View to list all jobs.
    """
    jobs = Job.objects.all()
    context = {
        "jobs": jobs,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/job_list.html", context)

def interview_list(request):
    """
    View to list all interviews, ordered by scheduled date.
    """
    interviews = Interview.objects.all().order_by("-scheduled_date")
    context = {
        "interviews": interviews,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/interview_list.html", context)

def placement_list(request):
    """
    View to list all placements.
    """
    placements = Placement.objects.all()
    context = {
        "placements": placements,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/placement_list.html", context)

# Create Views
def candidate_create(request):
    """
    View to create a new candidate with CV upload and parsing.
    """
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)

            # Handle CV upload and parsing
            cv_file = request.FILES.get('cv_file')
            if cv_file:
                cv_id, extracted_data = parse_and_store_cv(cv_file)
                candidate.cv = cv_id

                # Populate candidate fields with extracted data (if not already filled)
                if not candidate.full_name and extracted_data['full_name']:
                    candidate.full_name = extracted_data['full_name']
                    # Split full name into first_name and surname (basic split)
                    name_parts = extracted_data['full_name'].split(maxsplit=1)
                    candidate.first_name = name_parts[0]
                    candidate.surname = name_parts[1] if len(name_parts) > 1 else ''
                if not candidate.email and extracted_data['email']:
                    candidate.email = extracted_data['email']
                if not candidate.mobile and extracted_data['phone']:
                    candidate.mobile = extracted_data['phone']
                if not candidate.skills and extracted_data['skills']:
                    candidate.skills = extracted_data['skills']

            # Ensure required fields are set (e.g., candidate_id)
            if not candidate.candidate_id:
                candidate.candidate_id = str(uuid.uuid4())
            if not candidate.internal_cv_id:
                candidate.internal_cv_id = str(uuid.uuid4())
            if not candidate.agency_cv_id:
                candidate.agency_cv_id = str(uuid.uuid4())

            candidate.save()
            messages.success(request, "Candidate created successfully!")
            return redirect("recruitment:candidate_list")
    else:
        form = CandidateForm()
    context = {
        "form": form,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/candidate_form.html", context)

def company_create(request):
    """
    View to create a new company.
    """
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recruitment:company_list")
    else:
        form = CompanyForm()
    context = {
        "form": form,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/company_form.html", context)

def contact_create(request):
    """
    View to create a new contact.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recruitment:contact_list")
    else:
        form = ContactForm()
    context = {
        "form": form,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/contact_form.html", context)

def job_create(request):
    """
    View to create a new job.
    """
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.job_id = f"JOB-{Job.objects.count() + 1}"
            job.save()
            if not job.archived:
                wp_result = job.post_to_wordpress()
                messages.info(request, wp_result)
            messages.success(request, "Job created successfully!")
            return redirect("recruitment:job_list")
    else:
        form = JobForm(initial={'job_status': 'Briefed', 'commission_percentage': 10.00})
    next_job_id = Job.objects.count() + 1
    context = {
        "form": form,
        "next_job_id": next_job_id,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/job_form.html", context)

def placement_create(request):
    """
    View to create a new placement.
    """
    if request.method == "POST":
        form = PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recruitment:placement_list")
    else:
        form = PlacementForm()
    context = {
        "form": form,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/placement_form.html", context)

def interview_create(request):
    """
    View to create a new interview.
    """
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("recruitment:interview_list")
    else:
        form = InterviewForm()
    context = {
        "form": form,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/interview_form.html", context)

# Detail Views
def candidate_detail(request, pk):
    """
    View to display details of a specific candidate, including notes and CV.
    """
    candidate = get_object_or_404(Candidate, pk=pk)
    
    # Handle notes update
    if request.method == "POST" and 'notes' in request.POST:
        candidate.notes = request.POST.get('notes', '')
        candidate.save()
        messages.success(request, "Notes updated successfully!")
        return redirect('recruitment:candidate_detail', pk=pk)

    # Fetch CV content
    cv_data = get_cv_content(candidate.cv) if candidate.cv else None

    context = {
        "candidate": candidate,
        "cv_data": cv_data,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/candidate_detail.html", context)

def company_detail(request, pk):
    """
    View to display details of a specific company, including notes.
    """
    company = get_object_or_404(Company, pk=pk)
    
    # Handle notes update
    if request.method == "POST" and 'notes' in request.POST:
        company.notes = request.POST.get('notes', '')
        company.save()
        messages.success(request, "Notes updated successfully!")
        return redirect('recruitment:company_detail', pk=pk)

    context = {
        "company": company,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/company_detail.html", context)

def interview_detail(request, pk):
    """
    View to display details of a specific interview, including notes.
    """
    interview = get_object_or_404(Interview, pk=pk)
    
    # Handle notes update
    if request.method == "POST" and 'notes' in request.POST:
        interview.notes = request.POST.get('notes', '')
        interview.save()
        messages.success(request, "Notes updated successfully!")
        return redirect('recruitment:interview_detail', pk=pk)

    context = {
        "interview": interview,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/interview_detail.html", context)

def job_detail(request, pk):
    """
    View to display details of a specific job.
    """
    job = get_object_or_404(Job, pk=pk)
    context = {
        "job": job,
        "pomodoro": get_pomodoro_context(),
    }
    return render(request, "recruitment/job_detail.html", context)

# Helper Function
def get_user_emails(user):
    """
    Helper function to mock user emails.
    Replace with actual email fetching logic if needed.
    """
    return [
        {"subject": "Welcome!", "sender": "admin@example.com", "received_at": "2025-01-01 10:00"},
        {"subject": "New Tasks Assigned", "sender": "tasks@example.com", "received_at": "2025-01-02 14:00"},
    ]
