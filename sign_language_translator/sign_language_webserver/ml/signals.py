from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ML_Model, Evaluation


@receiver(post_save, sender=ML_Model)
def create_model(sender, instance, created, **kwargs):
    if created:
        Evaluation.objects.create(ml_model=instance)
