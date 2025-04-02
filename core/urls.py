# core/urls.py
from django.urls import path, include
from .views import home, dashboard, LinkedInProfileSearchAPIView
from .productivity_views import productivity_dashboard, board_detail, note_create, NoteViewSet
from .task_views import task_list, task_create, email_list, email_create  # Add email_create
from rest_framework.routers import DefaultRouter

app_name = 'core'

# Set up DRF router for ViewSets
router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('productivity/', productivity_dashboard, name='productivity_dashboard'),
    path('boards/<int:pk>/', board_detail, name='board_detail'),
    path('notes/create/', note_create, name='note_create'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('emails/', email_list, name='email_list'),
    path('emails/create/', email_create, name='email_create'),  # Add this
    path('api/linkedin/search/', LinkedInProfileSearchAPIView.as_view(), name='linkedin_search'),
    path('api/core/', include(router.urls)),
]
