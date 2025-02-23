# crm/utils.py
import requests
from django.conf import settings


def post_to_wordpress(job):
    """
    Post the job advert to WordPress using the REST API
    """
    wp_api_url = (
        settings.WORDPRESS_API_URL + "/wp-json/wp/v2/jobs"
    )  # Replace with your WordPress API endpoint
    auth = (
        settings.WORDPRESS_USER,
        settings.WORDPRESS_APP_PASSWORD,
    )  # Basic Auth credentials

    # Prepare the job data to be sent to WordPress
    data = {
        "title": job.title,
        "content": job.notes,  # The job advert (description)
        "status": (
            "publish" if job.publish_to_website else "draft"
        ),  # Publish or draft based on the job model
        "meta": {
            "company": job.company,
            "salary": str(job.salary),
            "day_rate": str(job.day_rate),
            "application_link": job.application_link,
            "category": job.category,
        },
    }

    # Attach the job spec file if available
    if job.job_spec:
        with open(job.job_spec.path, "rb") as file:
            files = {"file": file}
            response = requests.post(wp_api_url, auth=auth, data=data, files=files)
    else:
        response = requests.post(wp_api_url, auth=auth, data=data)

    # Check if the request was successful
    if response.status_code == 201:
        return "success"
    else:
        return f"Failed: {response.text}"
