import csv
from django.core.management.base import BaseCommand
from recruitment.models import Candidate


class Command(BaseCommand):
    help = "Load candidates and match them with their CV attachments"

    def handle(self, *args, **kwargs):
        # Load candidates.csv
        candidates_data = {}
        with open("candidates.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                candidate_id = row["candidate_id"]
                candidates_data[candidate_id] = {
                    "email": row["email"],
                    "full_name": row["full_name"],
                    "job_title": row.get("job_title", ""),
                    "recent_employer": row.get("recent_employer", ""),
                }

        # Load attachments.csv and merge with candidates
        with open("attachments.csv", "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                candidate_id = row["candidate_id"]
                if candidate_id in candidates_data:
                    candidates_data[candidate_id]["agency_cv_id"] = row["agency_cv_id"]
                    candidates_data[candidate_id]["internal_cv_id"] = row[
                        "internal_cv_id"
                    ]

        # Insert or update candidates in the database
        for candidate_id, data in candidates_data.items():
            candidate, created = Candidate.objects.update_or_create(
                candidate_id=candidate_id,
                defaults={
                    "email": data["email"],
                    "full_name": data["full_name"],
                    "job_title": data.get("job_title", ""),
                    "recent_employer": data.get("recent_employer", ""),
                    "agency_cv_id": data.get("agency_cv_id"),
                    "internal_cv_id": data.get("internal_cv_id"),
                },
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created new candidate: {candidate_id}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Updated existing candidate: {candidate_id}")
                )
