from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User
from django.conf import settings

@receiver(post_save, sender=User)
def notify_project_manager_on_employee_registration(sender, instance, created, **kwargs):
    if created and instance.is_employee:
        # Assuming 'is_projectmanager' is a boolean field on your User model
        project_managers = User.objects.filter(is_projectmanager=True)
        for pm in project_managers:
            # Here you'd implement your notification logic
            send_mail(
                'New Employee Registration',
                f'A new employee {instance.username} has registered and is awaiting approval.',
                settings.DEFAULT_FROM_EMAIL,
                [pm.email],
                fail_silently=False,
            )
