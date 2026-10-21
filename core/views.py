from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Grievance

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    # Role-Based Base Query
    if request.user.is_staff or request.user.is_superuser:
        base_qs = Grievance.objects.all().order_by('-created_at')
    else:
        base_qs = Grievance.objects.filter(student=request.user).order_by('-created_at')

    # Separate Active Queue from Resolved Archive
    active_grievances = base_qs.exclude(status='Resolved')
    resolved_grievances = base_qs.filter(status='Resolved')

    context = {
        'active_grievances': active_grievances,
        'resolved_grievances': resolved_grievances,
        'total': base_qs.count(),
        'pending': base_qs.filter(status='Pending').count(),
        'in_progress': base_qs.filter(status='In Progress').count(),
        'resolved': resolved_grievances.count(),
        'recent_pending': base_qs.filter(status='Pending')[:5],
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def submit_grievance(request):
    # Admin cannot lodge issues - redirect to dashboard if admin tries to access
    if request.user.is_staff or request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        priority = request.POST.get('priority', 'Medium')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')

        if title and description:
            Grievance.objects.create(
                student=request.user,
                title=title,
                category=category,
                priority=priority,
                status='Pending',
                description=description,
                attachment=attachment
            )
        return redirect('dashboard')
    return render(request, 'core/submit.html')

@login_required
def update_status(request, pk, new_status):
    if request.user.is_staff or request.user.is_superuser:
        grievance = get_object_or_404(Grievance, pk=pk)
        grievance.status = new_status
        grievance.save()
    return redirect('dashboard')