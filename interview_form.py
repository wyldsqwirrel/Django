# crm/forms/interview.py

from django import forms

from crm.models.candidate import Candidate
from crm.models.contact import Contact
from crm.models.interview import Interview

# crm/models/interview.py
new_candidate
new_candidate


class InterviewForm(forms.ModelForm):
    new_candidate = forms.BooleanField(
        required=False, label="Is this a new candidate?", initial=False
    )

    class Meta:
        model = Interview
        fields = [
            "job",
            "candidate",
            "new_candidate",
            "interviewer",
            "interview_type",
            "scheduled_date",
            "duration",
            "notes",
            "status",
            "feedback",
        ]

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.fields["job"].queryset = Job.objects.filter(is_active=True)

        self.fields["candidate"].queryset = Candidate.objects.filter(status="available")

        self.fields["interviewer"].queryset = Contact.objects.filter(role="interviewer")

    def save(self, *args, **kwargs):
        # Check if a new candidate is being created
        if self.cleaned_data.get("new_candidate"):
            # Create a new candidate based on the provided data (you can customize this as needed)
            new_candidate = Candidate.objects.create(
                full_name=self.cleaned_data["candidate"].strip(),
                email="new_candidate@example.com",  # Default email, update dynamically in the template if needed
                status="available",  # Ensure new candidate has an 'available' status by default
            )
            self.instance.candidate = new_candidate
            self.fields["candidate"].queryset = Candidate.objects.filter(
                status="available"
            )

        # Save the interview instance
        return super(InterviewForm, self).save(*args, **kwargs)
