from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:task_id>/update/', views.task_update, name='task_update'),
    path('emails/', views.email_list, name='email_list'),
    path('emails/create/', views.email_create, name='email_create'),
    path("run-task/", run_task, name="run_task"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("<int:pk>/delete/", task_delete, name="task_delete"),
    path("email-subtask/", email_subtask_completion, name="email_subtask_completion"),
    path("task-completed/", task_completed, name="task_completed"),
    path("create-subtask/", create_completed_subtask, name="create_completed_subtask"),
]
