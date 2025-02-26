from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('emails/', views.email_list, name='email_list'),
    path('emails/create/', views.email_create, name='email_create'),
    path('update_category/<int:task_id>/<str:category>/', views.update_category, name='update_category'),
    path('update_email_category/<int:email_id>/<str:category>/', views.update_email_category, name='update_email_category'),
    path('update_task_status/<int:task_id>/<str:status>/', views.update_task_status, name='update_task_status'),
]
