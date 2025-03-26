from django import forms
from .models import (
    Candidate,
    Company,
    Contact,
    Job,
    Placement,
    Interview,
    JobApplication,
)


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()


class CVUploadForm(forms.Form):
    doc_file = forms.FileField()
    docx_file = forms.FileField()
    pdf_file = forms.FileField()


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"


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
        fields = "__all__"


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "CV"]


class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = "__all__"


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@example.com"):  # Replace with valid domain
            raise forms.ValidationError("Only example.com emails are allowed!")
        return email
