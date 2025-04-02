# recruitment/admin.py
from django.contrib import admin
from .models import Candidate, Company, Contact, Job, Interview, Placement

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'candidate_status']  # Updated 'name' to 'full_name'
    list_filter = ['candidate_status']
    search_fields = ['full_name', 'email']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'industry']
    list_filter = ['industry']
    search_fields = ['name', 'email']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company']  # Updated 'name' to 'full_name'
    list_filter = ['company']
    search_fields = ['full_name', 'email']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'job_type', 'job_status']  # Updated 'name' to 'job_title', removed 'industry'
    list_filter = ['job_type', 'job_status']  # Removed 'industry'
    search_fields = ['job_title']

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['interview_id', 'job', 'candidate', 'status']
    list_filter = ['status', 'interview_type']
    search_fields = ['job__job_title', 'candidate__full_name']

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ['placement_code', 'job', 'candidate']  # Removed 'created_on'
    list_filter = ['placement_type']  # Removed 'created_on'
    search_fields = ['placement_code', 'job__job_title']
