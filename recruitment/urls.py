from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'recruitment'  # Namespace for URLs

from .views import (
    candidate_list,
    interview_list,
    company_list,
    contact_list,
    job_list,
    placement_list,
    placement_create,
    interview_create,
    candidate_create,
    company_create,
    contact_create,
    job_create,
    process_jobs_view,
)

urlpatterns = [  
    path("login/", LoginView.as_view(), name="auth_login"),
    path("interviews/", interview_list, name="interview_list"),
    path("interviews/new/", interview_create, name="interview_create"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("candidates/", candidate_list, name="candidate_list"),
    path("companies/", company_list, name="company_list"),
    path("contacts/", contact_list, name="contact_list"),
    path("jobs/", job_list, name="job_list"),
    path("process-jobs/", process_jobs_view, name="process_jobs"),
    path("placements/", placement_list, name="placement_list"),
    path("candidates/new/", candidate_create, name="candidate_create"),  # ✅ Fixed trailing slash
    path("companies/new/", company_create, name="company_create"),  # ✅ Fixed trailing slash
    path("contacts/new/", contact_create, name="contact_create"),  # ✅ Fixed trailing slash
    path("jobs/new/", job_create, name="job_create"),  # ✅ Fixed trailing slash
    path("placements/new/", placement_create, name="placement_create"),  # ✅ Fixed trailing slash
]
