from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import InterviewForm
from .models import Interview
from .models import Candidate, Company, Contact, Job, Placement, Interview, JobApplication
from .forms import (
    CandidateForm, CompanyForm, ContactForm, JobForm, PlacementForm, InterviewForm,
    CSVUploadForm, CVUploadForm, JobApplicationForm
)
import csv
from django.core.files.storage import default_storage

@login_required
def candidate_list(request):
    candidates = Candidate.objects.all()
    return render(request, "recruitment/candidate_list.html", {"candidates": candidates})

@login_required
def company_list(request):
    companies = Company.objects.all()
    return render(request, "recruitment/company_list.html", {"companies": companies})

@login_required
def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "recruitment/contact_list.html", {"contacts": contacts})

@login_required
def job_list(request):
    jobs = Job.objects.all()
    return render(request, "recruitment/job_list.html", {"jobs": jobs})

@login_required
def interview_list(request):
    interviews = Interview.objects.all()
    return render(request, "recruitment/interview_list.html", {"interviews": interviews})

@login_required
def placement_list(request):
    placements = Placement.objects.all()
    return render(request, "recruitment/placement_list.html", {"placements": placements})

@login_required
def job_application_list(request):
    applications = JobApplication.objects.all()
    return render(request, "recruitment/job_application_list.html", {"applications": applications})

@login_required
def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate created successfully!")
            return redirect("recruitment:candidate_list")
    else:
        form = CandidateForm()
    return render(request, "recruitment/candidate_form.html", {"form": form})

@login_required
def company_create(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Company created successfully!")
            return redirect("recruitment:company_list")
    else:
        form = CompanyForm()
    return render(request, "recruitment/company_form.html", {"form": form})

@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contact created successfully!")
            return redirect("recruitment:contact_list")
    else:
        form = ContactForm()
    return render(request, "recruitment/contact_form.html", {"form": form})

@login_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.post_to_wordpress()
            messages.success(request, "Job created and posted to WordPress!")
            return redirect("recruitment:job_list")
    else:
        form = JobForm()
    return render(request, "recruitment/job_form.html", {"form": form})

@login_required
def placement_create(request):
    if request.method == "POST":
        form = PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Placement created successfully!")
            return redirect("recruitment:placement_list")
    else:
        form = PlacementForm()
    return render(request, "recruitment/placement_form.html", {"form": form})

@login_required
def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview scheduled successfully!")
            return redirect("recruitment:interview_list")
    else:
        form = InterviewForm()
    return render(request, "recruitment/interview_form.html", {"form": form})

@login_required
def job_application_create(request):
    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Job application submitted successfully!")
            return redirect("recruitment:job_application_list")
    else:
        form = JobApplicationForm()
    return render(request, "recruitment/job_application_form.html", {"form": form})

@login_required
def csv_upload(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            file_path = default_storage.save(f'csv/{csv_file.name}', csv_file)
            full_path = default_storage.path(file_path)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        Candidate.objects.update_or_create(
                            candidate_id=row.get('candidate_id'),
                            defaults={
                                'first_name': row.get('first_name', ''),
                                'surname': row.get('surname', ''),
                                'full_name': f"{row.get('first_name', '')} {row.get('surname', '')}",
                                'email': row.get('email', ''),
                                'phone': row.get('phone', '')
                            }
                        )
                messages.success(request, "CSV uploaded and candidates processed!")
            except Exception as e:
                messages.error(request, f"Error processing CSV: {str(e)}")
            finally:
                default_storage.delete(file_path)  # Clean up
            return redirect("recruitment:candidate_list")
    else:
        form = CSVUploadForm()
    return render(request, "recruitment/csv_upload.html", {"form": form})

@login_required
def cv_upload(request):
    if request.method == "POST":
        form = CVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for field in ['doc_file', 'docx_file', 'pdf_file']:
                if form.cleaned_data[field]:
                    file = form.cleaned_data[field]
                    file_path = default_storage.save(f'cvs/{file.name}', file)
            messages.success(request, "CV files uploaded successfully!")
            return redirect("recruitment:candidate_list")
    else:
        form = CVUploadForm()
    return render(request, "recruitment/cv_upload.html", {"form": form})

@login_required
def interview_create(request):
    if request.method == "POST":
        form = InterviewForm(request.POST, request.FILES)
        if form.is_valid():
            interview = form.save()
            # Send email to candidate
            send_interview_email(interview)
            messages.success(request, f"Interview {interview.interview_id} scheduled for {interview.candidate.full_name}!")
            return redirect("recruitment:interview_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Check if job_id is passed in GET request for pre-filling
        job_id = request.GET.get('job_id')
        if job_id:
            try:
                job = Job.objects.get(id=job_id, archived=False)
                initial_data = {
                    'job': job,
                    'interview_type': 'VIR',  # Default value, adjust as needed
                    'stage': '1st',  # Default
                    'status': 'SCHEDULED',  # Default
                }
                form = InterviewForm(initial=initial_data)
            except Job.DoesNotExist:
                form = InterviewForm()
        else:
            form = InterviewForm()
    
    return render(request, "recruitment/interview_form.html", {"form": form})

def send_interview_email(interview):
    subject = f"Interview Scheduled: {interview.job.job_title}"
    message = (
        f"Dear {interview.candidate.full_name},\n\n"
        f"You have been scheduled for an interview for the position of {interview.job.job_title}.\n"
        f"Details:\n"
        f"- Date & Time: {interview.scheduled_date}\n"
        f"- Type: {interview.get_interview_type_display()}\n"
        f"- Stage: {interview.get_stage_display()}\n"
        f"Please prepare accordingly. Find attached the job specification and any relevant guides.\n\n"
        f"Best regards,\nRecruitment Team"
    )
    email = EmailMessage(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [interview.candidate.email],
    )
    # Attach files if they exist
    if interview.job_spec:
        email.attach_file(interview.job_spec.path)
    if interview.pdf_guides:
        email.attach_file(interview.pdf_guides.path)
    email.send(fail_silently=False)
