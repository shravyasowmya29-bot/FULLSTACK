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
    # Admins/Staff see all issues; regular students only see their own lodged tickets
    if request.user.is_staff or request.user.is_superuser:
        grievances = Grievance.objects.all().order_by('-created_at')
    else:
        grievances = Grievance.objects.filter(student=request.user).order_by('-created_at')

    context = {
        'grievances': grievances,
        'total': grievances.count(),
        'pending': grievances.filter(status='Pending').count(),
        'in_progress': grievances.filter(status='In Progress').count(),
        'resolved': grievances.filter(status='Resolved').count(),
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def submit_grievance(request):
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