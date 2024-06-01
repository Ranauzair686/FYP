from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from datetime import datetime

class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Yahan change karein
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    # Apne baki ke fields yahan add karein
    
    approval_status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    # Aur bhi fields add kar sakte hain as per your requirement
    # id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.user.username
    
class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')
    # Client-specific fields yahan add karein
    company_name = models.CharField(max_length=100)  # Example field
    # Aur bhi fields add kar sakte hain as per your requirement

    def __str__(self):
        return self.user.username
    
    
class User(AbstractUser):
    is_projectmanager = models.BooleanField('Is projectmanager', default=False)
    is_client = models.BooleanField('Is client', default=False)
    is_employee = models.BooleanField('Is employee', default=False)
    approval_status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied')], default='Pending')
    
# class SRS(models.Model):
#     client_name = models.CharField(max_length=100)
#     srs_document = models.FileField(upload_to='srs_uploads/')
#     upload_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.client_name} - {self.upload_date.strftime('%d/%m/%Y')}"


class ProjectTask(models.Model):
    project_name = models.CharField(max_length=100)
    project_description = models.TextField()
    srs_document = models.ForeignKey('SRS', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.project_name
class AssignedTask(models.Model):
    task = models.ForeignKey('ProjectTask', on_delete=models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    srs_document = models.ForeignKey('SRS', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.task.project_name} assigned to {self.employee.username} with SRS {self.srs_document}"

from django.db import models

class SRS(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    details = models.TextField()



    def __str__(self):
        return f"SRS from {self.client.username}: {self.details[:50]}"

from django.db import models

class AmbiguityDetectionResult(models.Model):
    text = models.TextField()
    detected_homonyms = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Detection Result from {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
