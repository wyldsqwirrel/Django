from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'recruitment'  # Namespace for URLs

from .views import (
    home,
    dashboard,
    candidate_list,
    interview_list,
    company_list,
    contact_list,
    job_list,
    placement_list,
    interview_create,
    candidate_create,
    company_create,
    contact_create,
    job_create,
    placement_create,
    apply_for_job,
    process_jobs_view,
    job_applied,
)

urlpatterns = [  
    path("login/", LoginView.as_view(), name="auth_login"),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("interviews/", interview_list, name="interview_list"),
    path("interviews/new/", interview_create, name="interview_create"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("candidates/", candidate_list, name="candidate_list"),
    path("companies/", company_list, name="company_list"),
    path("contacts/", contact_list, name="contact_list"),
    path("jobs/", job_list, name="job_list"),
    path("apply/<int:job_id>/", apply_for_job, name="apply_for_job"),
    path("process-jobs/", process_jobs_view, name="process_jobs"),
    path("job-applied/", job_applied, name="job_applied"),
    path("placements/", placement_list, name="placement_list"),
    path("candidates/new/", candidate_create, name="candidate_create"),  # ✅ Fixed trailing slash
    path("companies/new/", company_create, name="company_create"),  # ✅ Fixed trailing slash
    path("contacts/new/", contact_create, name="contact_create"),  # ✅ Fixed trailing slash
    path("jobs/new/", job_create, name="job_create"),  # ✅ Fixed trailing slash
    path("placements/new/", placement_create, name="placement_create"),  # ✅ Fixed trailing slash
]
