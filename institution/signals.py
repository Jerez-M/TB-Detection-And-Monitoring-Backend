from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Institution
from .institution_number import generate_institution_number

@receiver(post_save, sender=Institution)
def update_institution_number(sender, instance, created, **kwargs):
    if created:
        # Generate the initial institution_number on creation
        instance.institution_number = generate_institution_number(instance.institution_code, str(instance.pk), 4, 3)
        instance.save()
