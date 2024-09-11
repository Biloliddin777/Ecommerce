import json
import os
from datetime import datetime
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Product

@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, *args, **kwargs):
    if created:
        subject = 'New Product Created'
        message = f'Product "{instance.name}" has been created recently with price {instance.price}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['biloliddin14042009@gmail.com']
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False
        )

@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, *args, **kwargs):
    current_date = datetime.now()
    filename = os.path.join(settings.BASE_DIR, 'product/products_data', 'deleted_products.json')

    product_data = {
        'id': instance.id,
        'name': instance.name,
        'price': instance.price,
        'deleted_at': current_date.strftime('%Y-%m-%d %H:%M:%S')
    }

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            deleted_products = json.load(f)
    else:
        deleted_products = []

    deleted_products.append(product_data)

    with open(filename, mode='w') as f:
        json.dump(deleted_products, f, indent=4)

    print('Product successfully deleted and added to JSON file')

    subject = 'Product Deleted'
    message = f'Product "{instance.name}" has been deleted.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['biloliddin14042009@gmail.com']
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False
    )
