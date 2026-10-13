from django.db import models
from django.contrib.auth.models import User

class Grievance(models.Model):
    CATEGORY_CHOICES = [
        ('Lab/Hardware', 'Lab/Hardware'),
        ('Hostel/Facilities', 'Hostel/Facilities'),
        ('Academic', 'Academic'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grievances')
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    description = models.TextField()
    attachment = models.ImageField(upload_to='grievances/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id} {self.title} ({self.status})"