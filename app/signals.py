from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, TrainerUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.is_trainer:
        TrainerUser.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_trainer:
        if hasattr(instance, 'trainer_profile'):
            instance.trainer_profile.save()