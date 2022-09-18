from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from cart.models import Cart


User = get_user_model()


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()
