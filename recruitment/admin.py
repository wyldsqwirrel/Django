from django.contrib import admin
from .models import Company, Candidate, Job, Placement, Contact, Interview, JobApplication

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job_title', 'candidate_status', 'salary', 'created_at']
    list_filter = ['candidate_status', 'created_at', 'prefs']
    search_fields = ['full_name', 'email', 'job_title', 'skills']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'industry', 'company_size', 'created_at']
    list_filter = ['industry', 'created_at']
    search_fields = ['name', 'email', 'industry']

class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'company', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'email', 'company__name']

class JobAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'company', 'job_type', 'salary', 'rate', 'calculate_fee', 'created_at']
    list_filter = ['job_type', 'job_status', 'created_at']
    search_fields = ['job_title', 'company__name', 'skills_required']

    def calculate_fee(self, obj):
        return f"${obj.calculate_fee():,.2f}"
    calculate_fee.short_description = "Permanent Fee"

class PlacementAdmin(admin.ModelAdmin):
    list_display = ['placement_code', 'candidate', 'job', 'placement_type', 'start_date', 'permanent_base_salary', 'day_rate', 'calculate_fee', 'calculate_temp_fee', 'created_at']
    list_filter = ['placement_type', 'created_at']
    search_fields = ['candidate__full_name', 'job__job_title', 'placement_code']

    def calculate_fee(self, obj):
        return f"${obj.calculate_fee():,.2f}"
    calculate_fee.short_description = "Permanent Fee"

    def calculate_temp_fee(self, obj):
        return f"${obj.calculate_temp_fee():,.2f}"
    calculate_temp_fee.short_description = "Temp Fee"

class InterviewAdmin(admin.ModelAdmin):
    list_display = ['job', 'candidate', 'interview_type', 'stage', 'status', 'scheduled_date']
    list_filter = ['interview_type', 'stage', 'status', 'scheduled_date']
    search_fields = ['job__job_title', 'candidate__full_name']

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'job', 'submitted_at', 'app_status']
    list_filter = ['app_status', 'submitted_at']
    search_fields = ['full_name', 'email', 'job__job_title']

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Placement, PlacementAdmin)
admin.site.register(Interview, InterviewAdmin)
