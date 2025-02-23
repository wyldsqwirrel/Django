from celery import shared_task


@shared_task
def process_jobs():
    print("Processing jobs in the recruitment app")
    return "Jobs Processed"
