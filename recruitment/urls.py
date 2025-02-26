from django.urls import path
from . import views

app_name = 'recruitment'
urlpatterns = [
    path('jobs/', views.job_list, name='job_list'),  # Matches your earlier setup
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/create/', views.candidate_create, name='candidate_create'),
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create/', views.contact_create, name='contact_create'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('placements/', views.placement_list, name='placement_list'),
    path('placements/create/', views.placement_create, name='placement_create'),
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/create/', views.interview_create, name='interview_create'),
    path('applications/', views.job_application_list, name='job_application_list'),
    path('applications/create/', views.job_application_create, name='job_application_create'),
    path('csv-upload/', views.csv_upload, name='csv_upload'),
    path('cv-upload/', views.cv_upload, name='cv_upload'),
]
