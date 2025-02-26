from django.urls import path
from . import views

app_name = 'marketing'
urlpatterns = [
    path('', views.lead_list, name='lead_list'),
    path('lead/<int:lead_id>/', views.lead_detail, name='lead_detail'),
    path('lead/create/', views.lead_create, name='lead_create'),
    path('lead/<int:lead_id>/activity/', views.add_activity, name='add_activity'),
]
