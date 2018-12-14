from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Sender with signal; when user is saved send signal
# Received by receiver; create profile; takes args passed from post_save.


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
        if created:
                Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.profile.save()
