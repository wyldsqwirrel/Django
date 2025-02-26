from django.urls import path
from .views import dashboard  # Or a different view if intended

app_name = 'core_dashboard'  # Unique namespace
urlpatterns = [
    path('', dashboard, name='dashboard'),  # /dashboard/
]