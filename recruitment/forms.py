# recruitment/forms.py
from django import forms
from .models import Candidate, Company, Contact, Job, Placement, Interview, JobApplication

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class CVUploadForm(forms.Form):
    doc_file = forms.FileField()
    docx_file = forms.FileField()
    pdf_file = forms.FileField()

class CandidateForm(forms.ModelForm):
    cv_file = forms.FileField(required=False, label="Upload CV")

    class Meta:
        model = Candidate
        fields = "__all__"
        exclude = ['cv']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = "__all__"

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['company', 'contact', 'job_title', 'job_type', 'job_status', 'experience_level', 
                 'location', 'skills_required', 'job_description', 'salary', 'rate', 
                 'commission_percentage', 'archived']
        widgets = {
            'skills_required': forms.Textarea(attrs={'rows': 3}),
            'job_description': forms.Textarea(attrs={'rows': 5}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "CV"]

class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = "__all__"
