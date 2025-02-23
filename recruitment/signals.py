from django.db.models.signals import pre_save
from django.dispatch import receiver
from recruitment.models import Candidate


@receiver(pre_save, sender=Candidate)
def check_existing_candidate(sender, instance, **kwargs):
    existing_candidate = Candidate.objects.filter(
        agency_cv_id=instance.agency_cv_id
    ).first()

    if existing_candidate:
        # Prevent creating a duplicate by updating the existing record
        instance.id = existing_candidate.id  # Forces an update instead of insert
