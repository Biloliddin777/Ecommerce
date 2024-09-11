import json
import os
from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer

@receiver(post_save, sender=Customer)
def post_save_customer(sender, instance, created, *args, **kwargs):
    if created:
        print('After saving customer')
        subject = 'Customer saved'
        message = f'{instance.full_name} has been created recently'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['biloliddin14042009@gmail.com']
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

@receiver(pre_delete, sender=Customer)
def save_deleted_customer(sender, instance, *args, **kwargs):
    current_date = datetime.now()
    filename = os.path.join(settings.BASE_DIR, 'ecommerce/customers_data', 'deleted_customers.json')

    customer_data = {
        'id': instance.id,
        'full_name': instance.full_name,
        'email': instance.email,
        'phone': instance.phone,
        'address': instance.address,
        'image': str(instance.image),
        'slug': instance.slug,
        'deleted_at': current_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            deleted_customers = json.load(f)
    else:
        deleted_customers = []

    deleted_customers.append(customer_data)

    with open(filename, mode='w') as f:
        json.dump(deleted_customers, f, indent=4)

    print('Customer successfully deleted and added to JSON file')

    subject = 'Customer deleted'
    message = f'{instance.full_name} has been deleted.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['biloliddin14042009@gmail.com']
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
