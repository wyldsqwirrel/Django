# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.exceptions import TemplateDoesNotExist
from core.utils import get_pomodoro_context
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os

@login_required
def dashboard(request):
    """
    Dashboard view for the core app, displaying a summary and navigation links.
    """
    try:
        context = {
            'pomodoro': get_pomodoro_context(),
        }
        return render(request, 'core/dashboard.html', context)
    except TemplateDoesNotExist as e:
        return render(request, 'core/error.html', {'error_message': 'Dashboard template not found.'})

def home(request):
    """
    Home view for the core app, serving as the landing page.
    """
    try:
        context = {
            'pomodoro': get_pomodoro_context(),
        }
        return render(request, 'core/home.html', context)
    except TemplateDoesNotExist as e:
        return render(request, 'core/error.html', {'error_message': 'Home template not found.'})

class LinkedInProfileSearchAPIView(APIView):
    """
    API endpoint to search for LinkedIn profiles and fetch their URLs.
    """
    def get(self, request):
        # Get the search query from the request (e.g., person's name)
        query = request.query_params.get('query', None)

        if not query:
            return Response(
                {"error": "Query parameter 'query' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Proxycurl API configuration
        api_key = os.getenv('PROXYCURL_API_KEY')  # Store your API key in environment variables
        if not api_key:
            return Response(
                {"error": "Proxycurl API key not configured."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Proxycurl Person Search Endpoint
        url = "https://nubela.co/proxycurl/api/linkedin/profile/search"
        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        params = {
            'keyword': query,  # Search by keyword (e.g., person's name)
            'limit': 5,  # Limit to 5 results
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()

            # Extract LinkedIn profile URLs from the response
            profiles = data.get('profiles', [])
            profile_urls = [profile.get('linkedin_profile_url') for profile in profiles if profile.get('linkedin_profile_url')]

            return Response(
                {"linkedin_urls": profile_urls},
                status=status.HTTP_200_OK
            )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to fetch LinkedIn profiles: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
