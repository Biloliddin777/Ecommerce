import json
import os
from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'New User Created'
        message = f'New user created: {instance.email}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['biloliddin14042009@gmail.com']
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, *args, **kwargs):
    current_date = datetime.now()
    filename = os.path.join(settings.BASE_DIR, 'user/users_data', 'deleted_users.json')

    user_data = {
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'date_of_birth': instance.date_of_birth,
        'image': str(instance.image),
        'deleted_at': current_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            deleted_users = json.load(f)
    else:
        deleted_users = []

    deleted_users.append(user_data)

    with open(filename, mode='w') as f:
        json.dump(deleted_users, f, indent=4)

    print('User successfully deleted and added to JSON file')

    subject = 'User Deleted'
    message = f'User "{instance.email}" has been deleted.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['biloliddin14042009@gmail.com']
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
