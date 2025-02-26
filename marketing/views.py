from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lead, Activity
from tasks.models import Task
from datetime import timedelta

@login_required
def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'marketing/lead_list.html', {'leads': leads})

@login_required
def lead_detail(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    activities = lead.activities.all()
    return render(request, 'marketing/lead_detail.html', {'lead': lead, 'activities': activities})

@login_required
def lead_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST.get('phone', '')
        source = request.POST.get('source', '')
        lead = Lead(name=name, email=email, phone=phone, source=source, assigned_to=request.user)
        lead.save()
        # Initial activity: Lead Identified
        Activity.objects.create(lead=lead, activity_type="identified", description="Lead identified")
        Task.objects.create(
            title=f"Follow up with {lead.name}",
            assigned_to=request.user,
            due_by=lead.created_at + timedelta(days=2)
        )
        return redirect('marketing:lead_list')
    return render(request, 'marketing/lead_create.html')

@login_required
def add_activity(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if request.method == 'POST':
        activity_type = request.POST['activity_type']
        description = request.POST.get('description', '')
        activity = Activity(lead=lead, activity_type=activity_type, description=description)
        activity.save()
        # Create follow-up task for certain activities
        if activity_type in ['linkedin_request', 'email_sent', 'call_made', 'meeting_scheduled']:
            Task.objects.create(
                title=f"Follow up after {activity.get_activity_type_display()} for {lead.name}",
                assigned_to=request.user,
                due_by=activity.date + timedelta(days=3)
            )
        return redirect('marketing:lead_detail', lead_id=lead.id)
    return render(request, 'marketing/add_activity.html', {'lead': lead})
