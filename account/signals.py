from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order


@receiver(post_save, sender=Order)
def order_change_listener(sender, instance, created, **kwargs):
    if created:
        print(f"New order created: {instance}")
    else:
        print(f"Order updated: {instance}")
