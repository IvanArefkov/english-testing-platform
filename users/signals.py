from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.contrib.auth.models import User
from django.conf import settings

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            username=user.username,
        )

@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass

