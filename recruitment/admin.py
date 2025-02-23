from django.contrib import admin
from .models import Candidate, Job, Company, Contact, Placement  # ✅ Add all models here

# ✅ BaseAdmin class for shared filters & search
class BaseAdmin(admin.ModelAdmin):
    list_display = ["name", "created_on", "modified_on"]  # ✅ Standard fields for all models
    list_filter = ("created_on", "modified_on")  # ✅ Common filters
    search_fields = ("name", "created_on", "modified_on")  # ✅ Common search fields

# ✅ Register all models with BaseAdmin
@admin.register(Candidate)
class CandidateAdmin(BaseAdmin):
    list_display = ["name", "job_title", "candidate_status", "salary", "created_on"]
    list_filter = ("job_title", "candidate_status", "salary")
    search_fields = ("name", "job_title", "email", "skills", "industry", "created_on", "modified_on")

@admin.register(Job)
class JobAdmin(BaseAdmin):
    list_display = ["name", "industry", "salary", "created_on", "calculated_fee"]
    list_filter = ("industry", "salary")
    search_fields = ("name", "industry", "skills", "created_on", "modified_on")

    def calculated_fee(self, obj):
        return f"${obj.calculate_fee():,.2f}"  # ✅ Formats fee with commas
    calculated_fee.short_description = "Fee (Based on %)"  # ✅ Admin column title


@admin.register(Company)
class CompanyAdmin(BaseAdmin):
    list_display = ["name", "industry", "created_on"]
    list_filter = ("industry",)
    search_fields = ("name", "industry", "created_on", "modified_on")

@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ["name", "email", "created_on"]
    list_filter = ("created_on",)
    search_fields = ("name", "email", "created_on", "modified_on")

from django.contrib import admin
from .models import Placement

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ["candidate", "job", "created_on", "placement_type", "start_date", "calculated_fee", "calculated_temp_fee"]
    list_filter = ("created_on",)
    search_fields = ("candidate__full_name", "job__job_title", "created_on", "modified_on")

    def calculated_fee(self, obj):
        return f"${obj.calculate_fee():,.2f}"  # ✅ Formats fee correctly
    calculated_fee.short_description = "Placement Fee"

    def calculated_temp_fee(self, obj):
        return f"${obj.calculate_temp_fee():,.2f}"  # ✅ Formats temp fee correctly
    calculated_temp_fee.short_description = "Temp Placement Fee"
