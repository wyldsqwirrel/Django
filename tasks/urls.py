from django.urls import path
from tasks.views import (
    task_list,
    TaskViewSet,
    create_completed_subtask,
    email_subtask_completion,
    task_completed,
)
from .views import task_create
from tasks.views.task_delete import task_delete
from tasks.views.task_detail import task_detail
from tasks.views.run_task import run_task
from tasks.views.task_update import task_update
from tasks.views import TaskViewSet
from . import views

urlpatterns = [
    path("", task_list, name="task_list"),
    path("run-task/", run_task, name="run_task"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("new/", task_create, name="task_create"),
    path("<int:pk>/edit/", task_update, name="task_update"),
    path("<int:pk>/delete/", task_delete, name="task_delete"),
    path("email-subtask/", email_subtask_completion, name="email_subtask_completion"),
    path("task-completed/", task_completed, name="task_completed"),
    path("create-subtask/", create_completed_subtask, name="create_completed_subtask"),
]

from tasks.views.create_completed_subtask import create_completed_subtask
from tasks.views.create_completed_subtask import email_subtask_completion
from tasks.views.task_completed import task_completed
