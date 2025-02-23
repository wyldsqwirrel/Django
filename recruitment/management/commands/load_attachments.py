import csv
import os
from django.core.management.base import BaseCommand
from recruitment.models import Candidate

class Command(BaseCommand):
    help = "Load agency_cv_id and internal_cv_id from attachments.csv and update Candidates"
    

    def handle(self, *args, **kwargs):
        # Define the path to the CSV file
        csv_path = os.path.join(os.getcwd(), "attachments.csv")  # Adjust if needed

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR("attachments.csv file not found!"))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            updated_count = 0
            not_found_count = 0
            
            for row in reader:
                agency_cv_id = row.get("agency

                                       

Since **`agency_cv_id` and `internal_cv_id` are in `attachments.csv`**, and **`candidate_id` is in both `candidates.csv` and `attachments.csv`**, you need a script to **match and merge the data before inserting it into Django**.

---

## **Plan**
1. **Load `candidates.csv`** → Contains the main `Candidate` records.
2. **Load `attachments.csv`** → Contains `agency_cv_id` and `internal_cv_id`, matched using `candidate_id`.
3. **Merge data based on `candidate_id`** → Ensure each candidate gets the correct `agency_cv_id` and `internal_cv_id`.
4. **Insert or update data in Django** → Avoid duplicates.

---

## **1. Load and Merge CSV Files in Django**
Create a management command to process the files and update the database.

### **Step 1: Create a Management Command**
Run:
```bash
mkdir -p recruitment/management/commands
touch recruitment/management/commands/load_candidates.py
