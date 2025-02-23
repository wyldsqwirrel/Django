from django.contrib.auth.models import User
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.conf import settings  # ✅ Required for WordPress API
import requests  # ✅ Required for API call


GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]

import csv
import os


def get_default_cv():
    """Fetches the first CV ID from attachments.csv"""
    csv_path = os.path.join(settings.BASE_DIR, "recruitment/csv/attachments.csv")

    try:
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)  # Read CSV as dictionary
            for row in reader:
                return row["id"]  # ✅ Return the first available CV ID
    except (FileNotFoundError, KeyError):
        return None  # If no file or missing column, return None

def get_default_job():
    """Returns the first available Job ID or None if no jobs exist."""
    from recruitment.models import Job  # Avoid circular import issues
    return Job.objects.first().id if Job.objects.exists() else None


JOB_TYPE_CHOICES = [
    ("Full-time", "Full-time"),
    ("Part-time", "Part-time"),
    ("Contract", "Contract"),
    ("Freelance", "Freelance"),
]

CANDIDATE_STATUS_CHOICES = [
    ("active", "Active"),
    ("neutral", "Passive"),
    ("inactive", "Not Looking"),
    ("under_Offer", "Offered"),
    ("Placed", "Placed"),
    ("no_contact", "Do not contact")
]


# Candidate Model
class Candidate(models.Model):
    candidate_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    internal_cv_id = models.CharField(max_length=50, unique=True)
    agency_cv_id = models.CharField(max_length=50, unique=True)
    alternate_email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=20)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    recent_employer = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    prefs = models.CharField(
        max_length=50, choices=JOB_TYPE_CHOICES, default="Freelance"
     )

    candidate_status = models.CharField(max_length=50,choices=CANDIDATE_STATUS_CHOICES)
    skills = models.TextField()
    industry = models.CharField(max_length=100)
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    linkedin = models.URLField(blank=True, null=True)
    cv = models.CharField(max_length=50, unique=True, default=get_default_cv, null=True, blank=True)

# Company Model
class Company(models.Model):
    company_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    full_address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    company_size = models.IntegerField()
    industry = models.CharField(max_length=100)
    linkedin = models.URLField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Contact Model
class Contact(models.Model):
    contact_id = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    work_phone = models.CharField(max_length=20, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


# Job Model
from django.db import models
from django.conf import settings  # ✅ Required for WordPress API
import requests  # ✅ Required for API call


JOB_STATUS_CHOICES = [
    ("Briefed", "Briefed"),
    ("Interview_One", "Interview One"),
    ("Interview_Two", "Interview Two"),
    ("Interview_Final", "Final Interview"),
    ("Cancelled", "Cancelled"),
    ("Offer", "Offer"),
    ("Placed", "Placed"),
]

class Job(models.Model):
    job_id = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    job_status = models.CharField(
        max_length=50, choices=JOB_STATUS_CHOICES, default="Briefed"
    )
    experience_level = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    skills_required = models.TextField()
    job_description = models.TextField()
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # ✅ Salary for perm jobs
    rate = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)  # ✅ Hourly/daily rate for temp jobs
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # ✅ Default to 10%

    def calculate_fee(self):
        """Calculates the fee as a percentage of the salary (for permanent jobs)."""
        if self.salary and self.commission_percentage:
            return (self.salary * self.commission_percentage) / 100
        return 0.00

    def calculate_temp_fee(self):
        """Calculates the fee as a percentage of the day rate (for temporary jobs)."""
        if self.rate and self.commission_percentage:
            return (self.rate * self.commission_percentage) / 100
        return 0.00

    def post_to_wordpress(self):
        """
        Posts the job to WordPress via REST API.
        """
        wp_api_url = f"{settings.WORDPRESS_API_URL}/wp-json/wp/v2/jobs"
        auth = (settings.WORDPRESS_USER, settings.WORDPRESS_APP_PASSWORD)

        # ✅ Ensure only `salary` is posted (not rate)
        salary_display = f"<p><strong>Salary:</strong> ${self.salary:,.2f}</p>" if self.salary else ""

        data = {
            "title": self.job_title,
            "content": f"""
            <h3>About this Role</h3>
            <p>{self.job_description}</p>
            {salary_display}
            """,
            "status": "publish" if not self.archived else "draft",
        }

        try:
            response = requests.post(wp_api_url, auth=auth, json=data)
            response.raise_for_status()
            return "Job posted successfully to WordPress!"
        except requests.exceptions.RequestException as e:
            return f"Failed to post job: {str(e)}"

    def __str__(self):
        return self.job_title  # ✅ Only keep one `__str__()` method



class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    CV = models.FileField(upload_to="CVs/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("under_review", "Under Review"), ("accepted", "Accepted")],
        default="pending"
    )

    def __str__(self):
        return f"Application for {self.job.job_title} - {self.full_name}"


# Interview Model
INTERVIEW_TYPE_CHOICES = [
    ("F2F", "Face-to-Face"),
    ("VIR", "Virtual"),
    ("TEL", "Telephone"),
    ("OTH", "Other"),
]

INTERVIEW_STAGE_CHOICES = [
    ("1st", "Round 1"),
    ("2nd", "Round 2"),
    ("3rd", "Round 3"),
]

INTERVIEW_STATUS_CHOICES = [
    ("SCHEDULED", "Scheduled"),
    ("COMPLETED", "Completed"),
    ("CANCELLED", "Cancelled"),
    ("NO_SHOW", "No Show"),
]


class Interview(models.Model):
    interview_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="interviews")
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="interviews"
    )
    interviewer = models.ForeignKey(
        Contact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interviews",
    )
    interview_type = models.CharField(max_length=3, choices=INTERVIEW_TYPE_CHOICES)
    scheduled_date = models.DateTimeField(default=now)
    stage = models.CharField(max_length=3, choices=INTERVIEW_STAGE_CHOICES)
    status = models.CharField(max_length=20, choices=INTERVIEW_STATUS_CHOICES, default="SCHEDULED")
    feedback = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Interview {self.interview_id}: {self.job.job_title} | Candidate: {self.candidate.full_name}"

class Placement(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True, blank=True
    )
    placement_code = models.CharField(max_length=50, blank=True, unique=True)
    placement_type = models.CharField(
        max_length=15,
        choices=JOB_TYPE_CHOICES,  # Reuse the same choices
        verbose_name="Placement Type",
        default="Freelance",
    )
    start_date = models.DateField(null=True, blank=True)
    permanent_base_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    day_rate = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)  # ✅ Fix rate precision
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)  # Default 15%

    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)

    def calculate_fee(self):
        """Calculates the fee as a percentage of the permanent salary."""
        if self.permanent_base_salary and self.commission_percentage:
            return (self.permanent_base_salary * self.commission_percentage) / 100
        return 0.00

    def calculate_temp_fee(self):
        """Calculates the fee as a percentage of the daily rate."""
        if self.day_rate and self.commission_percentage:
            return (self.day_rate * self.commission_percentage) / 100
        return 0.00

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.job_title}"

    def save(self, *args, **kwargs):
        if self.job_id and not self.placement_code:
            self.placement_code = f"P{self.job_id}"
        super().save(*args, **kwargs)
